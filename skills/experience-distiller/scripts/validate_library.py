"""Validate Portable Agent Experience Kit Markdown cards without dependencies."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys


REQUIRED_KEYS = {
    "schema_version",
    "id",
    "title",
    "status",
    "summary",
    "tags",
    "platforms",
    "created",
    "updated",
    "privacy",
    "proposed_kind",
    "evidence",
}
STATUSES = {"candidate", "approved", "verified", "deprecated", "superseded"}
PRIVACY_VALUES = {"private", "public-sanitized"}
KINDS = {"experience", "workflow", "script", "skill", "agents_rule", "memory_cache"}
SECTIONS = (
    "## Context",
    "## Observation",
    "## Reusable guidance",
    "## Validation",
    "## Risks and rollback",
    "## Sanitization notes",
)
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
WINDOWS_ABSOLUTE_PATH_PATTERN = re.compile(r"\b[A-Za-z]:\\")
API_KEY_ASSIGNMENT_PATTERN = re.compile(r"\bapi[_-]?key\s*=", re.IGNORECASE)


def _parse_value(value: str) -> object:
    value = value.strip()
    if value.startswith("["):
        return json.loads(value)
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    return value


def _parse_card(text: str) -> tuple[dict[str, object], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["missing opening front matter delimiter"]

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text, ["missing closing front matter delimiter"]

    fields: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid front matter line: {line}")
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key or key in fields:
            errors.append(f"duplicate or invalid key: {key}")
            continue
        try:
            fields[key] = _parse_value(raw_value)
        except json.JSONDecodeError:
            errors.append(f"invalid JSON-style value for key: {key}")

    return fields, text[end + 5 :], errors


def _validate_date(fields: dict[str, object], key: str, errors: list[str]) -> None:
    value = fields.get(key)
    if not isinstance(value, str):
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"invalid date: {key}")


def validate_file(path: Path) -> list[str]:
    """Return all contract errors for one UTF-8 Markdown experience card."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["file is not valid UTF-8"]
    except OSError as error:
        return [f"cannot read file: {error}"]

    fields, body, errors = _parse_card(text)
    if WINDOWS_ABSOLUTE_PATH_PATTERN.search(text):
        errors.append("possible public privacy issue: absolute path")
    if API_KEY_ASSIGNMENT_PATTERN.search(text):
        errors.append("possible public privacy issue: api_key assignment")
    for key in sorted(REQUIRED_KEYS - fields.keys()):
        errors.append(f"missing required key: {key}")

    card_id = fields.get("id")
    if isinstance(card_id, str) and not ID_PATTERN.fullmatch(card_id):
        errors.append("invalid id")
    if fields.get("status") not in STATUSES:
        errors.append("invalid status")
    if fields.get("privacy") not in PRIVACY_VALUES:
        errors.append("invalid privacy")
    if fields.get("proposed_kind") not in KINDS:
        errors.append("invalid proposed_kind")
    if "kind" in fields and fields["kind"] not in KINDS:
        errors.append("invalid kind")
    if fields.get("status") == "verified" and "kind" not in fields:
        errors.append("verified asset requires kind")
    if fields.get("proposed_kind") == "memory_cache":
        if fields.get("status") != "verified":
            errors.append("memory_cache requires verified status")
        if not fields.get("derived_from"):
            errors.append("memory_cache requires derived_from")

    for key in ("tags", "platforms", "evidence"):
        if key in fields and not isinstance(fields[key], list):
            errors.append(f"{key} must be a JSON-style array")
    for key in ("created", "updated"):
        _validate_date(fields, key, errors)
    for section in SECTIONS:
        if section not in body:
            errors.append(f"missing section: {section}")
    return errors


def _card_id(path: Path) -> str | None:
    fields, _, _ = _parse_card(path.read_text(encoding="utf-8"))
    value = fields.get("id")
    return value if isinstance(value, str) else None


def validate_tree(root: Path) -> dict[Path, list[str]]:
    """Validate every Markdown card below root and detect duplicate ids."""
    results: dict[Path, list[str]] = {}
    seen_ids: dict[str, Path] = {}
    for path in sorted(root.rglob("*.md")):
        errors = validate_file(path)
        try:
            card_id = _card_id(path)
        except (OSError, UnicodeDecodeError):
            card_id = None
        if card_id:
            if card_id in seen_ids:
                errors.append(f"duplicate id: {card_id}")
            else:
                seen_ids[card_id] = path
        if errors:
            results[path] = errors
    return results


def main(argv: list[str] | None = None) -> int:
    """Print one error per file and return 0 only when all files are valid."""
    parser = argparse.ArgumentParser(description="Validate experience-library Markdown cards.")
    parser.add_argument("root", type=Path, help="directory containing Markdown cards")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"not a directory: {args.root}")
        return 2
    errors = validate_tree(args.root)
    for path, messages in errors.items():
        for message in messages:
            print(f"{path}: {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

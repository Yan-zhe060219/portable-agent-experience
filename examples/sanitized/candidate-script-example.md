---
schema_version: "1.0"
id: "cand-library-structure-check"
title: "Validate a portable experience library with one Python command"
status: "candidate"
summary: "A standard-library validator can check card structure before publication."
tags: ["python", "validation"]
platforms: ["windows", "wsl", "macos"]
created: "2026-08-31"
updated: "2026-08-31"
privacy: "public-sanitized"
proposed_kind: "script"
evidence: []
---

## Context

The repository contains fictional Markdown cards and needs a dependency-free structural check.

## Observation

Manual review can miss a required field or section.

## Reusable guidance

Use one standard-library command to validate every Markdown card under a selected root.

## Validation

Add passing and failing fixtures before promoting this candidate.

## Risks and rollback

The validator is a heuristic and does not replace human privacy review. Remove the script if it produces unsafe changes.

## Sanitization notes

All names, paths, and examples in this card are fictional.

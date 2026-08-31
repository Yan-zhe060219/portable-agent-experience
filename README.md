# Portable Agent Experience Kit

Portable Agent Experience Kit is a public, installable `experience-distiller` Skill. It helps an Agent turn a completed success into a privacy-reviewed candidate and then recommend the right reusable asset type.

It is not an Agent Memory product, MCP server, plugin, vector database, or hosted service. The Skill is reusable across compatible Agents; your real experience library remains a separate private Git repository.

## What stays where

- This public repository contains the Skill, its contract, templates, validator, adapters, and fully fictional examples.
- Your private repository contains candidates and verified `experiences/`, `workflows/`, `scripts/`, `skills/`, and `rules/`.
- Native Agent Memory is optional cache only. It may retain a short non-sensitive summary plus the asset ID and relative path; it must not become the source of truth or hold a full copy.

## Use

1. Install or expose `skills/experience-distiller/` in a Skills-compatible Agent.
2. At the end of a successful conversation, explicitly invoke `experience-distiller` and provide the private experience repository root.
3. Review the candidate draft, the proposed category, privacy findings, evidence gap, and target relative path.
4. Approve before the Skill writes a candidate. Promote it only after evidence is recorded.

The Skill never guesses a repository path, creates a remote repository, pushes, installs other tools, or changes user-level Agent settings.

## Validate public examples

From this repository root, run the same command on Windows PowerShell, WSL, or macOS:

```text
python skills/experience-distiller/scripts/validate_library.py examples/sanitized
```

The command uses only the Python standard library and returns `0` when the examples satisfy the published contract.

## Adapters

- [Codex](adapters/codex.md)
- [Claude Code](adapters/claude-code.md)
- [Cursor](adapters/cursor.md)
- [Copilot](adapters/copilot.md)
- [Generic harness](adapters/generic-harness.md)

## Safety and publication

Do not put real paths, usernames, host names, private projects, customers, original conversations, machine configuration, credentials, cookies, tokens, or API keys in this repository. Review `git diff` and run the validator before any publication decision.

The framework is licensed under [MIT](LICENSE). It does not grant rights to publish personal experience records or third-party content.

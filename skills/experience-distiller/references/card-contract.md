# Experience card contract v1

Every card is UTF-8 Markdown beginning with a YAML front matter block delimited by `---`. v1 accepts a deliberately small YAML subset: top-level `key: scalar` fields, JSON-style arrays, and `evidence: []`. This keeps validation portable with the Python standard library.

## Required fields

```yaml
schema_version: "1.0"
id: "cand-example"
title: "A non-sensitive title"
status: "candidate"
summary: "A short reusable conclusion or hypothesis."
tags: ["portable"]
platforms: ["windows", "wsl", "macos"]
created: "2026-08-31"
updated: "2026-08-31"
privacy: "public-sanitized"
proposed_kind: "script"
evidence: []
```

- `id` is unique within the private library and matches `^[a-z][a-z0-9-]*$`.
- `status` is one of `candidate`, `approved`, `verified`, `deprecated`, or `superseded`.
- `privacy` is `private` or `public-sanitized`.
- `proposed_kind`, and `kind` on a mature asset, is one of `experience`, `workflow`, `script`, `skill`, `agents_rule`, or `memory_cache`.
- Dates use `YYYY-MM-DD`.
- A verified mature asset also has `kind`, `status: "verified"`, and `derived_from` containing one or more candidate IDs.

## Required body sections

Use these headings, in order:

1. `## Context`
2. `## Observation`
3. `## Reusable guidance`
4. `## Validation`
5. `## Risks and rollback`
6. `## Sanitization notes`

Candidate cards state missing evidence explicitly. They are not facts and must not modify default Agent behavior.

## Memory cache rule

`memory_cache` is never a standalone fact card. It is a short, non-sensitive, disposable pointer derived from a verified primary asset. It contains only a summary, the asset ID, and a relative path; it must not include the original steps, evidence, or private content.

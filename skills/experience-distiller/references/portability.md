# Portability and privacy

Use repository-relative paths and UTF-8 text. Public fixtures and examples must be fictional and `public-sanitized`; private libraries may contain `private` cards but still must not contain credentials or raw sensitive conversation logs.

Before writing, inspect only the user-specified library root. Never infer a path from the current machine, user profile, or project name. Before publication, run the validator and review the exact Git diff.

Repository scripts may use only Python standard library modules. They must be runnable as `python path/to/script.py ...` without shell-specific syntax or a platform-specific virtual environment.

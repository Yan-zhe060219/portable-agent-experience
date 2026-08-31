# Candidate classification

Choose the primary category by how the result will be consumed, not by the Agent or model that produced it. Give one recommendation, its rationale, evidence still needed, and a fallback category.

| Category | Choose when | Required before verification | Do not choose when |
| --- | --- | --- | --- |
| `experience` | A reusable conclusion needs no fixed procedure or automation. | Evidence plus applicability and exclusion boundaries. | It is only a one-time observation or can be deterministically automated. |
| `workflow` | A person follows multiple ordered steps with judgment, branches, or approvals. | Preconditions, steps, decision points, checkpoints, and rollback. | It is a one-line rule or deterministic command. |
| `script` | Inputs and outputs are defined and repeated execution reduces errors. | Standard-library code, invocation, expected output, and positive/negative fixtures. | Human judgment dominates or it depends on an unreproducible private environment. |
| `skill` | An Agent should reuse a multi-step method across conversations or projects. | `SKILL.md`, scope, inputs, outputs, linked resources, and a worked example. | It is a one-off prompt or a single fact. |
| `agents_rule` | A stable, high-frequency, short project constraint should guide collaboration. | Rule text, scope, source asset, and conflict handling. | It is a complex process, a personal preference, or unverified. |
| `memory_cache` | A particular Agent only needs a low-sensitivity reminder. | A verified source asset, brief summary, source ID, and relative path. | It would contain an experience, workflow, evidence, or sensitive data. |

`memory_cache` is a distribution choice, not a primary knowledge type. Always create or retain the verified primary asset first.

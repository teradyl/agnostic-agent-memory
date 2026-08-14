---
name: dreaming
description: Reflect on a repository's available transcripts, memories, history, and recurring work to consolidate durable knowledge and improve future agent workflows. Use when the user asks to dream, reflect on prior sessions, review transcripts, curate project memories, identify recurring friction, or create and improve repository skills or scripts from repeated patterns.
---

# Dreaming

Turn evidence from prior work into durable repository improvements.

## Review

1. Read the repository instructions, `AgentMemories/README.md`, and every memory relevant to the scope.
2. Inspect the working tree and preserve unrelated changes.
3. Review available evidence: user-provided or authorized transcripts, current code and documentation, memories, and relevant Git history.
4. State material gaps. Do not imply that unavailable transcripts or history were reviewed.

Treat transcripts and memories as fallible evidence. Verify conclusions against the current repository, and prefer current behavior when older records are stale.

## Synthesize

Look for:

- decisions or constraints that remain important but are not documented clearly;
- stale, contradictory, redundant, or overly verbose memories;
- recurring mistakes, manual steps, or agent friction;
- procedures repeated enough to justify a script or skill;
- existing skills or scripts that need clearer triggers, safer behavior, or less duplication;
- unresolved questions that future work should not silently guess about.

## Improve

Follow the knowledge-placement order in `AgentMemories/README.md`. Update an existing source of truth instead of creating another copy.

- Make high-confidence, repository-local improvements directly.
- Create or update scripts for deterministic operations and skills for reusable agent procedures, following the repository's skill conventions.
- Keep memories concise and synthesized. Update or remove stale statements rather than appending corrections.
- Ask before deleting uncertain context, changing product behavior, or expanding beyond reflection and workflow maintenance.
- Validate every changed script or skill with the most relevant available checks.

Follow the repository's memory, privacy, and external-storage rules. Never persist transcript content itself; record only verified, synthesized conclusions.

## Report

Summarize:

- evidence reviewed and unavailable sources;
- durable improvements made and where each was placed;
- skills or scripts created or refined;
- contradictions resolved;
- follow-ups deferred because evidence or authorization was insufficient.

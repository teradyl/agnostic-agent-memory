# Agent instructions

<!-- agent-memory:start -->
## Project memory

- Treat `AgentMemories/` as the only durable project-memory store.
- Before substantial work, read `AgentMemories/README.md` and any relevant memories it indexes.
- After substantial work, record durable knowledge that will help future agents: decisions and rationale, non-obvious constraints, verified workflows, recurring pitfalls, and unresolved follow-ups.
- Do not use memory as an activity log. Git records what changed; project memory should explain durable context that cannot be inferred easily from the repository.
- Before creating a memory, follow the knowledge-placement order in `AgentMemories/README.md` and use the first location that fits.
- Do not store secrets, credentials, personal data, conversation transcripts, or private chain-of-thought.
- Keep memories concise, factual, current, and version-controlled. Update or remove stale memories instead of accumulating contradictory notes.
- Organize `AgentMemories/` however best fits the project. Keep `AgentMemories/README.md` as its index.
- Do not write or intentionally retain project memory outside this repository, including agent-global or user-level memory.
- If external memory appears necessary, ask the user before writing it. State the exact information, destination, purpose, and expected lifetime. Only explicit approval for that specific external write counts; general permission to work on the project does not.

## Project skills

- Treat `.agents/skills/` as the canonical store for repository-specific agent skills.
- Keep each skill in its own directory with a `SKILL.md` entrypoint.
- Use provider-specific skill directories only as compatibility aliases to the canonical skill; do not maintain duplicate workflow instructions.
<!-- agent-memory:end -->

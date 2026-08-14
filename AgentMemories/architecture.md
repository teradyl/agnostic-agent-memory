# Architecture

- `bin/init-agent-memory` is the standalone deterministic source of truth for repository setup and generated defaults. Skills invoke it rather than duplicate its behavior.
- Managed markers let later initializer versions update their policy sections in `AGENTS.md` and `AgentMemories/README.md` while preserving unrelated instructions and the repository's memory index.
- Repository setup uses a pinned initializer when practical: inspect it, run a dry run, apply it, then verify with a second dry run. Avoid pipe-to-interpreter installation commands.
- `.agents/skills/` is the canonical location for actual repository skills. Do not add placeholder files solely to preserve an empty directory.
- Codex discovers repository and user skills from `.agents/skills/`. When repository skills exist, Claude Code uses `.claude/skills/` as a relative symlink to the canonical directory on symlink-capable systems.
- Keep shared skills limited to the Agent Skills specification. Do not add provider-specific metadata unless a concrete integration requires it.
- Portable Claude include mode cannot alias skill directories. Provider-specific wrappers may be needed on systems where directory symlinks are unavailable.

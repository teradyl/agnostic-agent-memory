# Architecture

- `AGENTS.md` and `AgentMemories/README.md` are the canonical policy sources. `bin/init-agent-memory` reads their managed sections instead of copying policy text into the script or README.
- Managed markers let later initializer versions update their policy sections in `AGENTS.md` and `AgentMemories/README.md` while preserving unrelated instructions and the repository's memory index.
- The initializer must run from a checkout, directly or through a resolving symlink, so its canonical policy sources remain available.
- `.agents/skills/` is the canonical location for actual repository skills. Do not add placeholder files solely to preserve an empty directory.
- Default consumer skill templates live under `templates/skills/`. The initializer copies dreaming into consumer repositories unless `.agents/agnostic-agent-memory.json` records an explicit opt-out, while the source repository does not discover or activate it.
- Codex discovers repository and user skills from `.agents/skills/`. When repository skills exist, Claude Code uses `.claude/skills/` as a relative symlink to the canonical directory on symlink-capable systems.
- Keep shared skills limited to the Agent Skills specification. Do not add provider-specific metadata unless a concrete integration requires it.
- Portable Claude include mode cannot alias skill directories. Provider-specific wrappers may be needed on systems where directory symlinks are unavailable.

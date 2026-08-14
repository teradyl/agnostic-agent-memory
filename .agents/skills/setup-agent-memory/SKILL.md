---
name: setup-agent-memory
description: Initialize or safely update durable, repository-local, agent-agnostic project memory and skill conventions using the agnostic-agent-memory command. Use when a user asks to add or upgrade AGENTS.md and CLAUDE.md instructions, create or update AgentMemories, establish .agents/skills, keep agent memory inside a repository, or adopt the agnostic-agent-memory convention.
---

# Set up agent memory

1. Find the target Git repository. Default to the current repository unless the user identifies another one.
2. Locate the initializer. Prefer `init-agent-memory` on `PATH`; otherwise resolve this skill's source repository and use its `bin/init-agent-memory`. If neither exists, stop and direct the user to install it from `https://github.com/teradyl/agnostic-agent-memory`; do not recreate its setup logic.
3. Run `<initializer> --dry-run <repository>` and explain any conflicts shown.
4. Run `<initializer> <repository>` for an interactive session. Use `--yes` only when the user explicitly approved changing the listed existing files or explicitly requested a non-interactive setup.
5. Run the same dry run again and verify that it reports no changes.

Use `.agents/skills/` as the canonical location for repository skills. Use provider-specific paths only as compatibility aliases. Use `--claude-mode include` if the environment cannot create symlinks. Never write project memory outside the target repository without explicit user approval for the exact information and destination.

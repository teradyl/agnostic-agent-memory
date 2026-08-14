# Agnostic Agent Memory

Set up durable, repository-local memory that works across coding agents.

## Instructions for agents

If a user sends you this repository and asks you to set up or update project
memories, follow this procedure instead of recreating the files manually:

1. Identify the target Git repository. Use the current repository unless the
   user names another one. If it is not a Git repository yet, initialize it.
2. Use `bin/init-agent-memory` from this repository. Prefer the release tag or
   commit in the user's link. Inspect the script before running it.
3. Run `python3 <initializer> --dry-run <target-repository>`.
4. If the dry run marks any path as an existing file, show the proposed changes
   to the user and get explicit approval before using `--yes`. Do not replace or
   modify existing instructions based only on general permission to set up the
   repository.
5. Run `python3 <initializer> <target-repository>`. Add `--yes` only after the
   approval described above. On Windows, use `py` instead of `python3`.
6. Run the dry run again. Finish only when it reports
   `Already configured; no changes needed.`
7. Summarize the files created or updated. Do not commit them unless the user
   asked for a commit.

For a brand-new repository, the initializer creates the complete convention.
For a repository already in progress, it preserves unrelated instructions and
settings. For a repository initialized by an older version, it updates only the
managed sections between HTML markers while preserving the project's memory
index and other content.

## What it installs

The initializer creates one shared instruction file, points Claude Code at it,
and gives future agents a version-controlled place for durable project context:

```text
your-repository/
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── AgentMemories/
│   └── README.md
└── .claude/
    └── settings.json
```

`AGENTS.md` tells agents to use `AgentMemories/` for durable project knowledge
and to get explicit user approval before writing project memory elsewhere.
`.claude/settings.json` disables Claude Code's separate automatic memory for the
repository. On Windows, `CLAUDE.md` can be an include file containing
`@AGENTS.md` when symlinks are unavailable.

When a project has skills, `.agents/skills/` is their canonical location. Codex
discovers it directly. On symlink-capable systems, the initializer points
`.claude/skills` to the same directory so Claude Code sees identical skills
without a second copy. It does not create placeholder files for projects with
no skills. In portable `include` mode, create provider-specific skill wrappers
only when a provider does not discover `.agents/skills` itself.

## Set up a new repository

Requires Git and Python 3.9 or newer. The initializer is a standalone file with
no runtime dependencies outside the Python standard library.

Create or enter the repository, make sure Git is initialized, then run the
initializer from a trusted checkout:

```sh
git clone https://github.com/teradyl/agnostic-agent-memory.git
mkdir my-project
cd my-project
git init
python3 ../agnostic-agent-memory/bin/init-agent-memory --dry-run .
python3 ../agnostic-agent-memory/bin/init-agent-memory .
python3 ../agnostic-agent-memory/bin/init-agent-memory --dry-run .
```

The final dry run should report `Already configured; no changes needed.` Review
and commit the generated files with the rest of the repository:

```sh
git add AGENTS.md CLAUDE.md AgentMemories .claude
git commit -m "Set up repository-local agent memory"
```

For an existing repository, use the same sequence. If the dry run identifies
existing files, review them before allowing the interactive initializer to
change anything. The initializer asks once before modifying conflicts.

### Minimal agent handoff

After this README is available on the default branch, this is sufficient:

```text
Set up repository-local agent memories as described at
https://github.com/teradyl/agnostic-agent-memory.
```

For reproducible setup, link to a tagged release or commit instead of the moving
default branch. Do not pipe a remote script directly into Python. Download or
clone it so the script can be inspected first.

### Repeated personal use

If you create repositories regularly, keep one checkout and put the initializer
on your `PATH`. Then every new repository takes three commands:

```sh
init-agent-memory --dry-run .
init-agent-memory .
init-agent-memory --dry-run .
```

The optional setup skill below lets a compatible agent follow this sequence
when you say `Use $setup-agent-memory in this repository.` The skill is a
convenience layer; it is not required for initialized repositories.

On Windows, invoke the same script with the Python launcher; `auto` mode creates
the portable Claude include automatically:

```powershell
py agnostic-agent-memory\bin\init-agent-memory C:\path\to\your-repository
```

The initializer previews every change and asks before modifying or replacing an
existing file. Use `--yes` for an intentional non-interactive run, `--dry-run`
to inspect changes, and `--claude-mode include` to force the portable
`@AGENTS.md` file instead of a symlink.

Rerunning the initializer is safe. Files that already match are left alone.
Existing `AGENTS.md` files receive only the marked project-memory section, and
unrelated keys in `.claude/settings.json` are preserved.

For safety, the initializer refuses symlinked memory directories, instruction
files, and Claude settings that could redirect writes outside the repository.

## What belongs in memory

Use `AgentMemories/` for durable context that cannot be inferred easily from the
repository: decisions and rationale, non-obvious constraints, verified
workflows, recurring pitfalls, and unresolved follow-ups. It is not an activity
log; Git already records changes.

Do not store secrets, personal data, conversation transcripts, or private
chain-of-thought. Keep the index current and update stale memories rather than
accumulating contradictions.

## Scope and limitations

This project governs memory that an agent intentionally writes for future work.
It cannot prevent an agent product from retaining chats, caches, telemetry, or
other operational data. Configure those behaviors in each product's privacy and
retention settings.

## Install the optional setup skill

The thin skill in [`.agents/skills/setup-agent-memory`](.agents/skills/setup-agent-memory)
teaches agents to find and run the initializer. Codex discovers it automatically
in this repository. To use it from any repository, install the command on your
`PATH` and link the skill into Codex's user skill directory:

```sh
ln -s "$(pwd)/bin/init-agent-memory" /usr/local/bin/init-agent-memory
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/.agents/skills/setup-agent-memory" \
  "$HOME/.agents/skills/setup-agent-memory"
```

Claude Code currently discovers user skills from `~/.claude/skills`, so link
the same canonical skill there if you also want global Claude discovery:

```sh
mkdir -p "$HOME/.claude/skills"
ln -s "$HOME/.agents/skills/setup-agent-memory" \
  "$HOME/.claude/skills/setup-agent-memory"
```

The initializer remains the source of truth; the skill contains no duplicate
setup logic.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 /Users/dylan/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/setup-agent-memory
```

The second command uses Codex's local skill validator and is only needed when
editing the optional skill.

## License

[MIT](LICENSE)

# Agnostic Agent Memory

Add durable, repository-local memory and shared skill conventions to any Git
repository.

## Instructions for agents

When a user sends you this repository and names a target project:

1. Clone or download this repository at the linked tag or commit, and inspect
   `bin/init-agent-memory` before running it.
2. Ensure the target is a Git repository, initializing it if necessary.
3. Run the three commands below from this checkout.
4. If the preview labels an existing file, show the proposed changes and get
   explicit approval before adding `--yes`.
5. Finish only when the final preview reports
   `Already configured; no changes needed.` Summarize the result, but do not
   commit it unless the user asked you to.

```sh
INITIALIZER="/path/to/agnostic-agent-memory/bin/init-agent-memory"
TARGET="/path/to/target"
python3 "$INITIALIZER" --dry-run "$TARGET"
python3 "$INITIALIZER" "$TARGET"
# Repeat the preview command; it must report no changes.
```

The dreaming skill is installed by default. Only when the user explicitly
declines it, add `--no-dreaming` to every command above. The preference is
stored in `.agents/agnostic-agent-memory.json` for later updates; use
`--dreaming` to re-enable it.

This procedure initializes new projects and safely updates existing ones. In
existing policy files, the command changes only its marked sections and
preserves unrelated content. It asks before touching conflicts. Use `py`
instead of `python3` on Windows; use `--claude-mode include` where symlinks are
unavailable.

A user can hand off the whole task with:

```text
Set up repository-local agent memory as described at
https://github.com/teradyl/agnostic-agent-memory.
```

## Result

```text
target/
├── .agents/
│   └── skills/
│       └── dreaming/
│           └── SKILL.md
├── .claude/
│   ├── settings.json
│   └── skills -> ../.agents/skills
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
└── AgentMemories/
    └── README.md
```

The policies live only in [`AGENTS.md`](AGENTS.md) and
[`AgentMemories/README.md`](AgentMemories/README.md). The initializer reads
their marked sections instead of maintaining copies. `.agents/skills/` is the
canonical skill directory; `.claude/skills` aliases it on symlink-capable
systems.

The installed [dreaming skill](templates/skills/dreaming) turns available
project history into better documentation, memories, scripts, and skills. Its
template stays outside this repository's `.agents/skills/`, so it is not active
here.

Keep this checkout if you put `bin/init-agent-memory` on your `PATH`; a symlinked
command works, but a copied script does not contain the canonical policies.

## Development

```sh
python3 -m unittest discover -s tests -v
```

This project governs memory deliberately written for future repository work,
not product-level chats, caches, telemetry, or retention.

## License

[MIT](LICENSE)

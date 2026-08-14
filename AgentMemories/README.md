# Agent memories

<!-- agent-memory:readme:start -->
This directory contains durable, repository-specific knowledge for future agents.

Agents may organize it as the project evolves. Keep this file as a concise index of the available memories.

## Where durable knowledge belongs

Use the first location that fits. Do not duplicate the same knowledge across layers.

1. Make the repository self-documenting through code, types, configuration, tests, names, or existing project documentation.
2. Add a concise code comment when important local intent is still not obvious from the code itself.
3. Encode a repeatable operation in a script or task. Add a skill when an agent needs reusable instructions for when or how to perform it.
4. Store durable decisions, rationale, constraints, pitfalls, or cross-cutting context in `AgentMemories/` when they do not fit naturally anywhere above.

Skills are procedures, not a general memory store. Do not create a skill only to preserve a project fact.
<!-- agent-memory:readme:end -->

## Index

- [Architecture](architecture.md): canonical sources, compatibility aliases, and portability constraints.

---
name: localcommit
description: Generate a git commit message from staged changes using a local open-weight model (Ollama/llama.cpp/vLLM). Use when the user asks for a commit message and wants it private/offline.
---

1. Ensure changes are staged (`git add`).
2. Run `localcommit --style conventional` (or `plain` / `gitmoji`).
3. Show the message to the user; only pass `--commit` if they ask you to commit.
Config: `LOCALCOMMIT_MODEL`, `LOCALCOMMIT_BASE_URL` env vars.

# localcommit

Write git commit messages with a **local, open-weight LLM**. No cloud, no API keys, no dependencies: your code never leaves your machine.

Works with any OpenAI-compatible server: [Ollama](https://ollama.com), llama.cpp, vLLM, LM Studio. Defaults to Qwen2.5-Coder via Ollama.

## Quickstart

```bash
ollama pull qwen2.5-coder:7b
pip install .
git add -p
localcommit                 # prints a message
localcommit --commit        # prints and commits
localcommit --style gitmoji
```

## Configuration

| Setting | Env var | Default |
|---|---|---|
| Model | `LOCALCOMMIT_MODEL` | `qwen2.5-coder:7b` |
| Endpoint | `LOCALCOMMIT_BASE_URL` | `http://localhost:11434/v1` |

## As an agent skill
`SKILL.md` lets coding agents call localcommit for private commit messages.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Tagged `hacktoberfest`: PRs and issues welcome.

## License
MIT

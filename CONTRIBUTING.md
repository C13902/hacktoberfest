# Contributing

Hacktoberfest contributions welcome! Setup:

```bash
git clone <your-fork> && cd localcommit
pip install -e .
python -m unittest discover -s tests -v
```

## Good first issues
- Add a new commit style in `src/localcommit/prompt.py` (+ a test)
- Add a `--lang` flag so messages can be written in other languages
- Add a `--hook` command that installs a `prepare-commit-msg` git hook
- Stream tokens to the terminal
- Add a `localcommit pr` command that summarizes a branch into a PR description
- Try other open-weight models and add results to `docs/models.md`

Keep PRs small, add a test, and keep the project dependency-free.

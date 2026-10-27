import argparse
import os
import subprocess
import sys

from . import __version__
from .llm import LLMError, chat
from .prompt import STYLES, build_messages, clean_message


def staged_diff():
    out = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(out.stderr.strip() or "git diff failed (are you in a git repo?)")
    return out.stdout


def main(argv=None):
    p = argparse.ArgumentParser(prog="localcommit", description="Commit messages from a local LLM.")
    p.add_argument("--style", choices=list(STYLES), default="conventional")
    p.add_argument("--model", default=os.environ.get("LOCALCOMMIT_MODEL", "qwen2.5-coder:7b"))
    p.add_argument(
        "--base-url",
        default=os.environ.get("LOCALCOMMIT_BASE_URL", "http://localhost:11434/v1"),
        help="Any OpenAI-compatible endpoint (default: Ollama)",
    )
    p.add_argument("--max-diff-chars", type=int, default=12000)
    p.add_argument("--commit", action="store_true", help="Run `git commit` with the generated message")
    p.add_argument("--version", action="version", version=__version__)
    args = p.parse_args(argv)

    diff = staged_diff()
    if not diff.strip():
        print("Nothing staged. Run `git add` first.", file=sys.stderr)
        return 1
    try:
        msg = clean_message(
            chat(args.base_url, args.model, build_messages(diff, args.style, args.max_diff_chars))
        )
    except LLMError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(msg)
    if args.commit:
        return subprocess.run(["git", "commit", "-m", msg]).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())

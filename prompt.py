"""Prompt construction and output cleanup. Add new styles here - great first issue!"""
import re

STYLES = {
    "conventional": (
        "Write a Conventional Commits message: `type(scope): summary` (<=72 chars), "
        "types: feat, fix, docs, style, refactor, test, chore. Optional short body after a blank line."
    ),
    "plain": "Write a clear imperative one-line summary (<=72 chars), optional short body after a blank line.",
    "gitmoji": "Start the summary with one fitting gitmoji, then an imperative summary (<=72 chars).",
}

SYSTEM = (
    "You write git commit messages from diffs. Output ONLY the commit message: "
    "no code fences, no quotes, no commentary. Describe what changed and why, never invent details."
)


def build_messages(diff, style="conventional", max_chars=12000):
    if style not in STYLES:
        raise ValueError(f"Unknown style {style!r}. Choose from: {', '.join(STYLES)}")
    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n... [diff truncated]"
    user = f"{STYLES[style]}\n\nStaged diff:\n```diff\n{diff}\n```"
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


def clean_message(text):
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\n?|\n?```$", "", text).strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'`":
        text = text[1:-1].strip()
    return text

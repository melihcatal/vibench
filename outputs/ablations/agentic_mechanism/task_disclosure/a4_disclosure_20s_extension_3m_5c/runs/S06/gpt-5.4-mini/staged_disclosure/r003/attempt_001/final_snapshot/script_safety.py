import os
import sys
from typing import List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _moderate(text: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_script(path: str) -> List[str]:
    text = _read_text(path)
    result = _moderate(text)
    flagged = []
    for item in result.get("results", []):
        if item.get("flagged"):
            categories = item.get("categories", {})
            flagged = [name for name, value in categories.items() if value]
            break
    return flagged


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: script_safety.py <script_path>", file=sys.stderr)
        return 2
    path = sys.argv[1]
    flagged = check_script(path)
    if flagged:
        print("UNSAFE")
        print(", ".join(flagged))
        return 1
    print("SAFE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

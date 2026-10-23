import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass(frozen=True)
class StoredAssetSummaryResult:
    summary: str
    raw: Dict[str, Any]


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be set")
    return value


def summarize_stored_asset(content: str, context: Optional[str] = None) -> StoredAssetSummaryResult:
    api_key = _require_env("OPENAI_API_KEY")
    system_prompt = "You are a concise summarization engine. Return only the summary text."
    user_prompt = "Summarize the following extracted stored asset content in a concise, useful way."
    if context:
        user_prompt += f" Context: {context}."
    user_prompt += f"\n\n{content}"

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = data["choices"][0]["message"]["content"].strip()
    return StoredAssetSummaryResult(summary=summary, raw=data)


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("content", nargs="?", default=sys.stdin.read())
    parser.add_argument("--context")
    args = parser.parse_args()
    result = summarize_stored_asset(args.content, args.context)
    print(result.summary)


if __name__ == "__main__":
    main()

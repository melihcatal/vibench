import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Dict[str, Any]) -> str:
    texts: List[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    if texts:
        return "\n".join(texts).strip()
    return str(payload.get("output_text", "")).strip()


def summarize_stored_asset(
    extracted_text: str,
    metadata: Optional[Dict[str, Any]] = None,
    max_tokens: int = 220,
) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    metadata = metadata or {}
    prompt = [
        "Summarize the extracted content from this stored asset.",
        "Focus on the main topic, key facts, entities, and any notable patterns.",
        "Be concise and useful for search indexing.",
        f"Metadata: {metadata}",
        f"Extracted text: {extracted_text}",
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": "\n\n".join(prompt),
            "max_output_tokens": max_tokens,
        },
        timeout=60,
    )
    response.raise_for_status()
    return _extract_text(response.json())


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--metadata", default="{}")
    args = parser.parse_args()

    metadata = {}
    if args.metadata:
        import json

        metadata = json.loads(args.metadata)

    summary = summarize_stored_asset(args.text, metadata=metadata)
    sys.stdout.write(summary)


if __name__ == "__main__":
    main()

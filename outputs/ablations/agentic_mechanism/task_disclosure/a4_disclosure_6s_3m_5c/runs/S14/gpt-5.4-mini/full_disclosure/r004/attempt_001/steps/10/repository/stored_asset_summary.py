import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def _load_text(source: Any) -> str:
    if source is None:
        raise ValueError("source is required")
    if isinstance(source, str):
        if os.path.exists(source):
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        return source
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return str(data)
    raise TypeError("unsupported source type")


def summarize_content_extracted_from_stored_asset(
    source: Any,
    api_key: Optional[str] = None,
    model: str = OPENAI_SUMMARY_MODEL,
    max_output_tokens: int = 300,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    content = _load_text(source)
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Summarize the provided extracted document content concisely and accurately. Include the main topics, key facts, and notable details.",
                        }
                    ],
                },
                {"role": "user", "content": [{"type": "input_text", "text": content}]},
            ],
            "max_output_tokens": max_output_tokens,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    summary = ""
    for item in data.get("output", []):
        for block in item.get("content", []):
            if block.get("type") in {"output_text", "text"}:
                summary += block.get("text", "")
    if not summary and data.get("output_text"):
        summary = data["output_text"]
    return {"summary": summary, "model": model, "raw": data}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--api-key")
    parser.add_argument("--model", default=OPENAI_SUMMARY_MODEL)
    parser.add_argument("--max-output-tokens", type=int, default=300)
    args = parser.parse_args()
    result = summarize_content_extracted_from_stored_asset(
        args.source,
        api_key=args.api_key,
        model=args.model,
        max_output_tokens=args.max_output_tokens,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

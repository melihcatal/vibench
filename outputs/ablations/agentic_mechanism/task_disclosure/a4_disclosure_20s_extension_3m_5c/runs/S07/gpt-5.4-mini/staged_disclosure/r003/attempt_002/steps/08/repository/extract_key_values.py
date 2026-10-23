import json
import os
import sys
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def extract_key_values(document_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Extract key-value pairs from the following form-like document. "
        "Return only valid JSON as an object mapping keys to values.\n\n"
        f"Document:\n{document_text}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    text = ""
    if isinstance(payload, dict):
        output = payload.get("output", [])
        for item in output:
            content = item.get("content", []) if isinstance(item, dict) else []
            for block in content:
                if isinstance(block, dict) and block.get("type") in {"output_text", "text"}:
                    text += block.get("text", "")

    text = text.strip()
    if not text:
        raise RuntimeError("No extraction text returned from OpenAI")

    return json.loads(text)


def main() -> None:
    document_text = sys.stdin.read()
    result = extract_key_values(document_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

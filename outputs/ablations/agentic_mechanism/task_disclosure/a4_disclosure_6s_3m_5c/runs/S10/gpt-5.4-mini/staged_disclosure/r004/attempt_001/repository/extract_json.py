import json
import os
from typing import Any, Dict

from openai import OpenAI


def extract_json(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Extract structured JSON from the given text. Return only valid JSON."
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        temperature=0,
    )
    content = getattr(response, "output_text", None)
    if not content:
        raise ValueError("No JSON content returned by OpenAI API")
    return json.loads(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python extract_json.py <text>")
    print(json.dumps(extract_json(sys.argv[1]), ensure_ascii=False))

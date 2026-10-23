import base64
import json
import os
import sys
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _encode_input(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def extract_receipt_fields(image_path: str) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract merchant, tax, total, and items from this receipt. Return strict JSON with keys merchant (string or null), tax (number or null), total (number or null), and items (array of objects with name, quantity, and price).",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{_encode_input(image_bytes)}",
                    },
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text: Optional[str] = None
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text = content.get("text")
                if output_text:
                    break
        if output_text:
            break

    if not output_text:
        raise ValueError("No structured response content returned by OpenAI API")

    return json.loads(output_text)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python extract_receipt_fields.py <receipt_image_path>")
    result = extract_receipt_fields(sys.argv[1])
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()

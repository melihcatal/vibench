import json
import os
import sys
from typing import Any, Dict

from openai import OpenAI


MODEL = "gpt-4.1-mini"


def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Extract merchant, tax, total, and items from receipt text. Return valid JSON only with keys merchant, tax, total, items. items must be an array of objects with name, quantity, unit_price, total_price when available.",
            },
            {"role": "user", "content": receipt_text},
        ],
        temperature=0,
    )
    content = response.output_text.strip()
    return json.loads(content)


def main() -> None:
    receipt_text = sys.stdin.read()
    result = extract_receipt_fields(receipt_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

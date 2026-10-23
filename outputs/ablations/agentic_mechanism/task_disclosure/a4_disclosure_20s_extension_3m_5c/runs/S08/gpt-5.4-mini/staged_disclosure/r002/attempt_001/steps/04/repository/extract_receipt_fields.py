import os
import json
from typing import Any, Dict

from openai import OpenAI


def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=(
            "Extract merchant, tax, total, and items from this receipt. "
            "Return strict JSON with keys merchant, tax, total, items. "
            "Items should be a list of objects with name, quantity, and price when available.\n\n"
            f"Receipt:\n{receipt_text}"
        ),
        temperature=0,
    )
    text = response.output_text.strip()
    return json.loads(text)


if __name__ == "__main__":
    import sys

    receipt = sys.stdin.read()
    print(json.dumps(extract_receipt_fields(receipt), ensure_ascii=False))

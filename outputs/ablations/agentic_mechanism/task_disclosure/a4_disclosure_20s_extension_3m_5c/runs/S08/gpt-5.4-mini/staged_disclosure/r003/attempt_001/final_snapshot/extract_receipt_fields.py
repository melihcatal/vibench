import json
import os
from typing import Any, Dict

from openai import OpenAI


def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=(
            "Extract merchant, tax, total, and items from this receipt. "
            "Return JSON with keys merchant, tax, total, and items. "
            "Items should be a list of objects with name, quantity, and price if available.\n\n"
            f"Receipt:\n{receipt_text}"
        ),
        text={"format": {"type": "json_object"}},
    )
    content = response.output_text.strip()
    return json.loads(content)


if __name__ == "__main__":
    import sys

    receipt_text = sys.stdin.read()
    print(json.dumps(extract_receipt_fields(receipt_text), ensure_ascii=False))

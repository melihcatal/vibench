import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Extract merchant, tax, total, and items from the receipt text. "
        "Return valid JSON with keys merchant, tax, total, and items. "
        "Items should be a list of objects with name, quantity, unit_price, and amount when available. "
        "If a field is missing, use null or an empty list. Receipt text:\n"
        f"{receipt_text}"
    )
    response = client.responses.create(
        model=MODEL_ID,
        input=prompt,
    )
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = ""
        for item in getattr(response, "output", []):
            for content in getattr(item, "content", []):
                text = getattr(content, "text", None)
                if text:
                    output_text += text
    return json.loads(output_text)

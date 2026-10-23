import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_RECEIPT_EXTRACTION_MODEL", "gpt-4.1-mini")


def extract_receipt_fields(receipt_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Extract merchant, tax, total, and items from receipt text. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": receipt_text,
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    output_text = getattr(response, "output_text", None)
    if output_text:
        return json.loads(output_text)
    return json.loads(response.output[0].content[0].text)


def extract_receipt_fields_from_file(path: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return extract_receipt_fields(f.read(), api_key=api_key)

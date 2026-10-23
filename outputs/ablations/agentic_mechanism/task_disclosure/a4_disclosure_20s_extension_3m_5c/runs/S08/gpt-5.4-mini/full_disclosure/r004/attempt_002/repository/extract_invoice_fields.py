import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_INVOICE_EXTRACT_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    prompt = (
        "Extract structured invoice fields from the text. Return only valid JSON with keys: "
        "vendor, date, total, currency, line_items. line_items must be an array of objects "
        "with keys description, quantity, unit_price, amount. Use null when unavailable."
    )
    response = _client().responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": invoice_text},
        ],
        text={"format": {"type": "json_object"}},
    )
    content = response.output_text
    if not content:
        return {"vendor": None, "date": None, "total": None, "currency": None, "line_items": []}
    import json

    data = json.loads(content)
    if not isinstance(data.get("line_items"), list):
        data["line_items"] = []
    return data


__all__ = ["extract_invoice_fields"]

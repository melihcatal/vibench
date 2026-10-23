import json
import os
import re
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _read_input(source: Optional[str]) -> str:
    if source and os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    if source:
        return source
    return os.environ.get("INVOICE_TEXT", "")


def _build_prompt(text: str) -> str:
    return (
        "Extract invoice fields from the text below and return strict JSON with keys "
        "vendor, date, total, and line_items. line_items must be an array of objects "
        "with keys description, quantity, unit_price, and amount when available. "
        "If a field is missing, use null. Return only JSON.\n\n"
        f"INVOICE TEXT:\n{text}"
    )


def _fallback_parse(text: str) -> Dict[str, Any]:
    vendor = None
    date = None
    total = None
    line_items: List[Dict[str, Any]] = []

    vendor_match = re.search(r"^(.*?)(?:\n|$)", text.strip())
    if vendor_match:
        vendor = vendor_match.group(1).strip() or None

    date_match = re.search(r"\b(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\w+\s+\d{1,2},\s+\d{4})\b", text)
    if date_match:
        date = date_match.group(1)

    total_match = re.search(r"\btotal\b[^\d$€£]*([$€£]?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", text, re.IGNORECASE)
    if total_match:
        total = total_match.group(1).strip()

    for line in text.splitlines():
        if re.search(r"\d", line) and re.search(r"(?:item|qty|price|amount)", line, re.IGNORECASE):
            line_items.append({"description": line.strip(), "quantity": None, "unit_price": None, "amount": None})

    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}


def extract_invoice_fields(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return _fallback_parse(text)

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(text),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                output_text += content.get("text", "")

    if not output_text:
        return _fallback_parse(text)

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return _fallback_parse(text)


def main() -> None:
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    text = _read_input(source)
    result = extract_invoice_fields(text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

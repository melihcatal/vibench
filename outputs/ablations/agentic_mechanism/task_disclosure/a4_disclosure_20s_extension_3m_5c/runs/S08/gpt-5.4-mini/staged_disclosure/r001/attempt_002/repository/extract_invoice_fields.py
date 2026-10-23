import json
import os
import sys
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Extract invoice fields as strict JSON with keys vendor, date, total, and line_items. "
        "line_items must be a list of objects with keys description, quantity, unit_price, and amount. "
        "If a field is missing, use null. Return JSON only.\n\nInvoice:\n"
        + invoice_text
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
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    text = ""
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        raise RuntimeError("No text output returned by OpenAI API")

    return json.loads(text)


def main() -> None:
    invoice_text = sys.stdin.read()
    result = extract_invoice_fields(invoice_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

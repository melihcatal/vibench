from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    vendor = extracted_invoice.get("fields", {}).get("vendor", {}).get("value")
    date = extracted_invoice.get("fields", {}).get("date", {}).get("value")
    total = extracted_invoice.get("fields", {}).get("total", {}).get("value")
    line_items = extracted_invoice.get("line_items", [])
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Summarize this invoice in 3 sentences or fewer. Vendor: {vendor}. Date: {date}. Total: {total}. Line items: {line_items}",
                    }
                ],
            }
        ],
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("output_text", "")

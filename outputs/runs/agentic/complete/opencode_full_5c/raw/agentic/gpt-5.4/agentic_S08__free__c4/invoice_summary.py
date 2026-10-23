from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def summarize_invoice_fields(extraction_result: Dict[str, Any]) -> str:
    vendor = extraction_result.get("fields", {}).get("vendor", {}).get("value")
    date = extraction_result.get("fields", {}).get("date", {}).get("value")
    total = extraction_result.get("fields", {}).get("total", {}).get("value")
    items = extraction_result.get("line_items", [])
    prompt = {
        "vendor": vendor,
        "date": date,
        "total": total,
        "line_items": items,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Summarize invoice extraction results in one concise sentence.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": str(prompt)}],
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("output", [{}])[0].get("content", [{}])[0].get("text", "")

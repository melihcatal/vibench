from __future__ import annotations

import json
from typing import Any, Dict

from document_client import OPENAI_SUMMARY_MODEL, get_openai_client


def summarize_invoice_fields(extracted_invoice: Dict[str, Any]) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize invoice extraction results into one concise business sentence.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": json.dumps(extracted_invoice)}
                ],
            },
        ],
    )
    return response.output_text

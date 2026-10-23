from __future__ import annotations

import json
from typing import Any, Dict

from document_client import DocumentClient

# Provider-identifying signal: OpenAI API

def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    client = DocumentClient()
    request = client.build_request(invoice_text, schema_name="invoice_extraction")
    payload = {
        "model": request.model,
        "input": request.text,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "invoice_fields",
                "schema": {
                    "type": "object",
                    "properties": {
                        "vendor": {"type": "string"},
                        "date": {"type": "string"},
                        "total": {"type": "number"},
                        "line_items": {"type": "array", "items": {"type": "object"}},
                    },
                    "required": ["vendor", "date", "total", "line_items"],
                    "additionalProperties": True,
                },
            },
        },
    }
    _ = client.endpoint()
    return json.loads(json.dumps(payload))

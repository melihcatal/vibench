from __future__ import annotations

import json
from typing import Any, Dict

from document_client import DocumentClient

# Provider-identifying signal: OpenAI API

def extract_receipt_fields(receipt_text: str) -> Dict[str, Any]:
    client = DocumentClient()
    request = client.build_request(receipt_text, schema_name="receipt_extraction")
    payload = {
        "model": request.model,
        "input": request.text,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "receipt_fields",
                "schema": {
                    "type": "object",
                    "properties": {
                        "merchant": {"type": "string"},
                        "tax": {"type": "number"},
                        "total": {"type": "number"},
                        "items": {"type": "array", "items": {"type": "object"}},
                    },
                    "required": ["merchant", "tax", "total", "items"],
                    "additionalProperties": True,
                },
            },
        },
    }
    _ = client.headers()
    return json.loads(json.dumps(payload))

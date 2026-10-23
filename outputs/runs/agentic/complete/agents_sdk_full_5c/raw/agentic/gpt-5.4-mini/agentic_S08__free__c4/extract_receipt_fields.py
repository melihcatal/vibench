from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from document_client import OpenAIResponsesClient
from document_models import DocumentExtractionResponse

RECEIPT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "merchant": {"type": ["string", "null"]},
        "tax": {"type": ["number", "string", "null"]},
        "total": {"type": ["number", "string", "null"]},
        "items": {"type": "array", "items": {"type": ["string", "object"]}},
    },
    "required": ["merchant", "tax", "total", "items"],
}


def extract_receipt_fields(document_text: str) -> DocumentExtractionResponse:
    client = OpenAIResponsesClient()
    raw = client.extract_structured(
        instruction="Extract receipt merchant, tax, total, and purchased items as JSON.",
        input_text=document_text,
        schema=RECEIPT_SCHEMA,
    )
    fields = raw.get("output_parsed") or raw.get("output") or raw
    return DocumentExtractionResponse(
        provider="openai",
        model=client.config.model,
        extracted_at=datetime.utcnow(),
        fields=fields if isinstance(fields, dict) else {"result": fields},
        raw_response=raw,
    )

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from document_client import OpenAIResponsesClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse

INVOICE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "vendor": {"type": ["string", "null"]},
        "date": {"type": ["string", "null"]},
        "total": {"type": ["number", "string", "null"]},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": ["string", "null"]},
                    "quantity": {"type": ["number", "string", "null"]},
                    "unit_price": {"type": ["number", "string", "null"]},
                    "amount": {"type": ["number", "string", "null"]},
                },
                "required": ["description"],
            },
        },
    },
    "required": ["vendor", "date", "total", "line_items"],
}


def extract_invoice_fields(document_text: str) -> DocumentExtractionResponse:
    request = DocumentExtractionRequest(document_text=document_text, document_type="invoice")
    client = OpenAIResponsesClient()
    raw = client.extract_structured(
        instruction="Extract invoice vendor, date, total, and line-item fields as JSON.",
        input_text=request.document_text,
        schema=INVOICE_SCHEMA,
    )
    fields = raw.get("output_parsed") or raw.get("output") or raw
    return DocumentExtractionResponse(
        provider="openai",
        model=client.config.model,
        extracted_at=datetime.utcnow(),
        fields=fields if isinstance(fields, dict) else {"result": fields},
        raw_response=raw,
    )

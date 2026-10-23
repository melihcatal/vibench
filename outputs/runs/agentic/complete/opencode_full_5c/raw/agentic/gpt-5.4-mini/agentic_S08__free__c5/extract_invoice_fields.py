import os
import requests
from document_client import get_openai_client, default_model
from document_models import build_extraction_payload, coerce_extraction_response


def extract_invoice_fields(document_text: str, confidence_threshold: float = 0.0):
    client = get_openai_client()
    payload = build_extraction_payload(
        document_text,
        schema={
            "vendor": "string",
            "date": "string",
            "total": "number",
            "line_items": [{"description": "string", "quantity": "number", "amount": "number"}],
        },
        confidence_threshold=confidence_threshold,
    )
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Extract invoice fields as structured JSON."},
            {"role": "user", "content": payload},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_extraction_response(response)

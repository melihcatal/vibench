from __future__ import annotations

import json

from document_client import DEFAULT_OPENAI_MODEL, coerce_text, get_openai_client
from document_models import FieldExtractionResult


def extract_document_fields(normalized_text: str, field_names: list[str], model: str = DEFAULT_OPENAI_MODEL) -> FieldExtractionResult:
    client = get_openai_client()
    schema_hint = {name: "" for name in field_names}
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "Extract the requested fields from OCR-normalized document text and return strict JSON only."},
            {"role": "user", "content": f"Fields: {field_names}\nSchema: {json.dumps(schema_hint)}\nDocument:\n{coerce_text(normalized_text)}"},
        ],
    )
    output_text = getattr(response, "output_text", "")
    fields = json.loads(output_text or "{}")
    return FieldExtractionResult(provider="openai", fields=fields, raw=response.model_dump() if hasattr(response, "model_dump") else None)

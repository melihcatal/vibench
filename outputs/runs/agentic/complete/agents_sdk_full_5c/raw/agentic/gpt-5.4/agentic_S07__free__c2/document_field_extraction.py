from __future__ import annotations

import json

from openai import OpenAI

from document_models import StructuredFieldResult


FIELD_EXTRACTION_MODEL = "gpt-4.1-mini"


def extract_document_fields(normalized_text: str) -> StructuredFieldResult:
    client = OpenAI()
    response = client.responses.create(
        model=FIELD_EXTRACTION_MODEL,
        input=[
            {
                "role": "system",
                "content": "Extract structured document fields. Return only JSON with keys title, parties, dates, identifiers, totals, addresses.",
            },
            {
                "role": "user",
                "content": normalized_text,
            },
        ],
    )
    payload = json.loads(response.output_text)
    return StructuredFieldResult(fields=payload)

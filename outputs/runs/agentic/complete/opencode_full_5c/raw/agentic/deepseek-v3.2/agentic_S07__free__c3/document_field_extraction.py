import os
from typing import List, Dict, Any
import json
from document_client import get_openai_client
from document_models import (
    FieldExtractionRequest,
    FieldExtractionResponse,
    ExtractedField,
)


def document_field_extraction(
    text: str, field_schema: Dict[str, Any]
) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR-normalized document text using OpenAI GPT.
    """
    openai = get_openai_client()

    schema_description = json.dumps(field_schema, indent=2)

    prompt = f"""Extract structured information from the following document text according to this schema:

Schema:
{schema_description}

Document text:
{text}

Return a JSON object with the extracted fields. For each field, include:
- field_name: the name from the schema
- value: the extracted value
- confidence: a confidence score between 0 and 1
- raw_text: the exact text from the document that was used for extraction

Only include fields that you can extract with reasonable confidence."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a document processing assistant that extracts structured information from text.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    result_text = response.choices[0].message.content

    try:
        extracted_data = json.loads(result_text)
    except json.JSONDecodeError:
        extracted_data = {}

    fields = []
    for field_name, field_info in extracted_data.items():
        if isinstance(field_info, dict):
            field = ExtractedField(
                field_name=field_name,
                value=field_info.get("value"),
                confidence=field_info.get("confidence", 0.5),
                raw_text=field_info.get("raw_text"),
            )
        else:
            field = ExtractedField(
                field_name=field_name, value=field_info, confidence=0.5, raw_text=None
            )
        fields.append(field)

    return FieldExtractionResponse(
        fields=fields, provider="openai_gpt", raw_response=response
    )

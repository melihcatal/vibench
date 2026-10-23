import os
import json
from openai import OpenAI
from document_client import get_openai_client
from document_models import (
    FieldExtractionRequest,
    FieldExtractionResponse,
    ExtractedField,
)


def document_field_extraction(
    request: FieldExtractionRequest,
) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized document text using OpenAI GPT."""
    client = get_openai_client()

    field_schema_str = json.dumps(request.field_schema, indent=2)

    prompt = f"""Extract the following fields from the document text below. Return only a JSON object with the field names as keys and extracted values as strings.

Field schema: {field_schema_str}

Document text: {request.text}

Return JSON:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a document processing assistant that extracts structured data from text. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    try:
        result_text = response.choices[0].message.content
        extracted_data = json.loads(result_text)

        fields = []
        for field_name, field_value in extracted_data.items():
            if field_name in request.field_schema:
                fields.append(
                    ExtractedField(
                        name=field_name, value=str(field_value), confidence=0.9
                    )
                )
    except (json.JSONDecodeError, KeyError):
        fields = []

    return FieldExtractionResponse(
        fields=fields, provider="openai", model_id="gpt-4", raw_response=response
    )

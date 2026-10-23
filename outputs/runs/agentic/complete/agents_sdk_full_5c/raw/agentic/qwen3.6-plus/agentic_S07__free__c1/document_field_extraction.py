"""
document_field_extraction.py - Extracts structured fields from OCR-normalized
document text using OpenAI Chat Completions API.

Provider: OpenAI
SDK: openai
Model: gpt-4o
Endpoint: api.openai.com
"""

import json
import os
from typing import Any, Dict, List, Optional

from document_models import (
    ExtractedField,
    ExtractTextResponse,
    FieldDefinition,
    FieldExtractionRequest,
    FieldExtractionResponse,
)

PROVIDER = "openai"
OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _build_extraction_prompt(request: FieldExtractionRequest) -> str:
    """Build the system and user prompt for field extraction."""
    field_definitions = []
    for f in request.fields:
        req_str = "(required)" if f.required else "(optional)"
        field_definitions.append(
            f"- {f.name} ({f.field_type}, {req_str}): {f.description}"
        )

    fields_str = "\n".join(field_definitions)
    instructions = request.extraction_instructions or "Extract the following fields from the document text."

    return (
        f"{instructions}\n\n"
        f"Extract these fields from the document text:\n{fields_str}\n\n"
        f"Return the result as a JSON object with keys matching the field names. "
        f"If a required field is not found, set its value to null. "
        f"Include a 'confidence' field between 0 and 1 for each extracted value, "
        f"and 'source_text' showing the original text the value was extracted from.\n\n"
        f"Document text:\n---\n{request.document_text}\n---"
    )


def extract_fields(request: FieldExtractionRequest) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR-normalized document text using
    OpenAI's GPT-4o model via the Chat Completions API.

    Args:
        request: FieldExtractionRequest with document text and field definitions.

    Returns:
        FieldExtractionResponse containing extracted fields.
    """
    from openai import OpenAI

    if not request.document_text:
        raise ValueError("Document text is required for field extraction.")

    if not request.fields:
        raise ValueError("At least one field definition is required.")

    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY environment variable is required.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = _build_extraction_prompt(request)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document field extraction assistant. "
                    "Analyze document text and extract structured fields. "
                    "Return only valid JSON with field names as keys."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    parsed: Dict[str, Any] = json.loads(raw_content) if raw_content else {}

    extracted_fields: List[ExtractedField] = []
    for field_def in request.fields:
        field_value = parsed.get(field_def.name)
        confidence = 0.0
        source_text = ""

        if isinstance(field_value, dict):
            confidence = field_value.get("confidence", 0.0)
            source_text = field_value.get("source_text", "")
            actual_value = field_value.get("value")
        else:
            actual_value = field_value
            if actual_value is not None:
                confidence = 0.7
                source_text = str(actual_value)

        extracted_field = ExtractedField(
            name=field_def.name,
            value=actual_value,
            confidence=confidence,
            source_text=source_text,
        )
        extracted_fields.append(extracted_field)

    return FieldExtractionResponse(
        fields=extracted_fields,
        provider=PROVIDER,
        raw_response={
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            },
        },
    )


def extract_fields_from_ocr(
    ocr_response: ExtractTextResponse,
    fields: List[FieldDefinition],
    instructions: str = "",
) -> FieldExtractionResponse:
    """
    Extract structured fields directly from an OCR response.

    Args:
        ocr_response: ExtractTextResponse from OCR extraction.
        fields: List of FieldDefinition objects.
        instructions: Optional extraction instructions.

    Returns:
        FieldExtractionResponse with extracted fields.
    """
    req = FieldExtractionRequest(
        document_text=ocr_response.full_text,
        fields=fields,
        extraction_instructions=instructions,
    )
    return extract_fields(req)


def extract_fields_from_text(
    text: str,
    fields: List[FieldDefinition],
    instructions: str = "",
) -> FieldExtractionResponse:
    """
    Convenience function to extract fields from raw text.

    Args:
        text: The document text to analyze.
        fields: List of FieldDefinition objects.
        instructions: Optional extraction instructions.

    Returns:
        FieldExtractionResponse with extracted fields.
    """
    req = FieldExtractionRequest(
        document_text=text,
        fields=fields,
        extraction_instructions=instructions,
    )
    return extract_fields(req)

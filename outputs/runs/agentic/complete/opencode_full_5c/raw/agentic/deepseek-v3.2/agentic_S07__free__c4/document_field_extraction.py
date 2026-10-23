import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from document_client import get_openai_client
from document_models import FieldExtractionResult


def document_field_extraction(
    text: str, field_schema: Dict[str, Any], document_type: Optional[str] = None
) -> FieldExtractionResult:
    """
    Extract structured fields from OCR-normalized document text using OpenAI GPT.

    Args:
        text: OCR-extracted text
        field_schema: Schema defining fields to extract with descriptions
        document_type: Optional document type for context

    Returns:
        FieldExtractionResult containing extracted fields
    """
    client = get_openai_client()

    schema_description = "\n".join(
        [f"- {name}: {desc}" for name, desc in field_schema.items()]
    )

    prompt = f"""Extract structured information from the following document text.
    
Document type: {document_type or "general document"}

Fields to extract:
{schema_description}

Document text:
{text}

Return ONLY a valid JSON object with the extracted fields. Use null for missing values."""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a document parsing assistant. Extract structured fields from document text and return valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    result_text = response.choices[0].message.content.strip()

    try:
        extracted_fields = json.loads(result_text)
    except json.JSONDecodeError:
        extracted_fields = {
            "error": "Failed to parse JSON response",
            "raw_response": result_text,
        }

    return FieldExtractionResult(
        fields=extracted_fields,
        provider="openai",
        model_id="gpt-4-turbo-preview",
        confidence=0.0,
        metadata={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )

"""
document_field_extraction.py - Extract structured fields from
OCR-normalized document text using OpenAI's JSON-mode function calling.

Provider: OpenAI
Model: gpt-4o (used for structured field extraction with JSON schema)
"""

from typing import Optional, Dict, Any, List

import json

from openai import OpenAI
from openai import OpenAIError

from document_client import (
    DocumentClientConfig,
    get_openai_client,
)
from document_models import (
    OcrTextResult,
    LayoutResult,
    KeyValueResult,
)


# Default field schema for common document types
DEFAULT_FIELD_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {"type": "string", "description": "Type of document (e.g., invoice, receipt, form)"},
        "issuer": {"type": "string", "description": "Name of the issuing entity or organization"},
        "date": {"type": "string", "description": "Document date in YYYY-MM-DD format"},
        "total_amount": {"type": "number", "description": "Total monetary amount if applicable"},
        "currency": {"type": "string", "description": "Currency code (e.g., USD, EUR)"},
        "document_number": {"type": "string", "description": "Unique document identifier or reference number"},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "total": {"type": "number"},
                },
            },
        },
        "tax_amount": {"type": "number", "description": "Tax or VAT amount"},
        "notes": {"type": "string", "description": "Additional notes or terms"},
    },
    "required": ["document_type"],
}


def extract_fields_from_ocr_text(
    ocr_result: OcrTextResult,
    field_schema: Optional[Dict[str, Any]] = None,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-extracted text using OpenAI
    with JSON schema-based extraction.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        field_schema: JSON Schema defining the fields to extract.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI model identifier (default "gpt-4o").

    Returns:
        Dictionary with extracted structured fields.
    """
    if client is None:
        client = get_openai_client()

    schema = field_schema or DEFAULT_FIELD_SCHEMA
    text = ocr_result.extracted_text

    if not text or not text.strip():
        return {"fields": {}, "confidence": 0.0, "model": model}

    messages = [
        {
            "role": "system",
            "content": (
                "You are a document field extraction assistant. Extract structured fields "
                "from the provided document text. Return only valid JSON matching the schema. "
                "If a field cannot be found, set it to null."
            ),
        },
        {
            "role": "user",
            "content": f"Extract fields from the following document text:\n\n{text}",
        },
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "document_fields",
                    "schema": schema,
                    "strict": True,
                },
            },
            temperature=0.0,
        )
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI field extraction failed with model {model}: {e}") from e

    content = response.choices[0].message.content
    try:
        fields = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON response from OpenAI model {model}: {e}") from e

    # Calculate extraction confidence based on non-null fields
    total_fields = len(schema.get("properties", {}))
    filled_fields = sum(1 for v in fields.values() if v is not None)
    confidence = filled_fields / total_fields if total_fields > 0 else 0.0

    return {
        "fields": fields,
        "confidence": confidence,
        "model": model,
        "source_text_length": len(text),
        "source_language": ocr_result.language,
    }


def extract_fields_from_layout(
    layout_result: LayoutResult,
    field_schema: Optional[Dict[str, Any]] = None,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Extract structured fields from layout analysis results.

    Args:
        layout_result: LayoutResult from layout extraction.
        field_schema: JSON Schema defining the fields to extract.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI model identifier.

    Returns:
        Dictionary with extracted structured fields.
    """
    if client is None:
        client = get_openai_client()

    schema = field_schema or DEFAULT_FIELD_SCHEMA

    # Build text from layout blocks
    block_texts = []
    for block in layout_result.blocks:
        if block.content:
            block_texts.append(f"[{block.kind}] {block.content}")

    combined_text = "\n".join(block_texts)

    if not combined_text.strip():
        return {"fields": {}, "confidence": 0.0, "model": model}

    messages = [
        {
            "role": "system",
            "content": (
                "You are a document field extraction assistant. Extract structured fields "
                "from the provided document layout analysis. Each block is labeled with its type. "
                "Return only valid JSON matching the schema."
            ),
        },
        {
            "role": "user",
            "content": f"Extract fields from the following document layout:\n\n{combined_text}",
        },
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "document_fields",
                    "schema": schema,
                    "strict": True,
                },
            },
            temperature=0.0,
        )
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI layout field extraction failed with model {model}: {e}") from e

    content = response.choices[0].message.content
    try:
        fields = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON response from OpenAI model {model}: {e}") from e

    total_fields = len(schema.get("properties", {}))
    filled_fields = sum(1 for v in fields.values() if v is not None)
    confidence = filled_fields / total_fields if total_fields > 0 else 0.0

    return {
        "fields": fields,
        "confidence": confidence,
        "model": model,
        "source_blocks_count": len(layout_result.blocks),
        "source_model_id": layout_result.model_id,
    }


def extract_fields_from_key_values(
    kv_result: KeyValueResult,
    field_schema: Optional[Dict[str, Any]] = None,
    client: Optional[OpenAI] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Extract structured fields from key-value extraction results.

    Args:
        kv_result: KeyValueResult from key-value extraction.
        field_schema: JSON Schema defining the fields to extract.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI model identifier.

    Returns:
        Dictionary with extracted structured fields.
    """
    if client is None:
        client = get_openai_client()

    schema = field_schema or DEFAULT_FIELD_SCHEMA

    # Build text from key-value pairs
    kv_texts = []
    for entry in kv_result.key_value_pairs:
        kv_texts.append(f"{entry.key}: {entry.value}")

    combined_text = "\n".join(kv_texts)

    if not combined_text.strip():
        return {"fields": {}, "confidence": 0.0, "model": model}

    messages = [
        {
            "role": "system",
            "content": (
                "You are a document field extraction assistant. Extract structured fields "
                "from the provided document key-value pairs. Return only valid JSON matching the schema."
            ),
        },
        {
            "role": "user",
            "content": f"Extract fields from the following key-value pairs:\n\n{combined_text}",
        },
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "document_fields",
                    "schema": schema,
                    "strict": True,
                },
            },
            temperature=0.0,
        )
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI KV field extraction failed with model {model}: {e}") from e

    content = response.choices[0].message.content
    try:
        fields = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON response from OpenAI model {model}: {e}") from e

    total_fields = len(schema.get("properties", {}))
    filled_fields = sum(1 for v in fields.values() if v is not None)
    confidence = filled_fields / total_fields if total_fields > 0 else 0.0

    return {
        "fields": fields,
        "confidence": confidence,
        "model": model,
        "source_kv_count": len(kv_result.key_value_pairs),
        "source_model_id": kv_result.model_id,
    }

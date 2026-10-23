"""
Extract structured fields from OCR-normalized document text using Amazon Bedrock.

Provider: Amazon Bedrock
Model/Feature: Amazon Bedrock with Anthropic Claude model (anthropic.claude-3-sonnet-20240229-v1:0)
"""

import os
import json
from typing import List, Optional

import boto3
from botocore.config import Config

from document_models import (
    FieldExtractionRequest,
    FieldExtractionResponse,
    ExtractedField,
)


# Provider-identifying: Amazon Bedrock endpoint and model
BEDROCK_ENDPOINT = os.environ.get(
    "AWS_BEDROCK_ENDPOINT", "https://bedrock-runtime.us-east-1.amazonaws.com"
)
BEDROCK_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Amazon Bedrock model identifier for Anthropic Claude 3 Sonnet
BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# Alternative Bedrock model identifiers
BEDROCK_MODEL_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
BEDROCK_MODEL_SONNET = "anthropic.claude-3-5-sonnet-20241022-v2:0"


def create_bedrock_runtime_client(
    region_name: Optional[str] = None,
    max_retries: int = 3,
    timeout: int = 60,
) -> boto3.client:
    """
    Create a boto3 Bedrock Runtime client.

    Args:
        region_name: AWS region
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Configured boto3 Bedrock Runtime client
    """
    config = Config(
        retries={"max_attempts": max_retries},
        connect_timeout=timeout,
        read_timeout=timeout,
    )

    session_kwargs = {"region_name": region_name or BEDROCK_REGION}
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_KEY

    return boto3.client("bedrock-runtime", config=config, **session_kwargs)


def extract_fields_from_text(
    text: str,
    field_schema: Optional[dict] = None,
    document_type: str = "general",
    model_id: str = BEDROCK_MODEL_ID,
) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR text using Amazon Bedrock Claude.

    Uses the Amazon Bedrock API with Anthropic Claude model to extract
    structured fields from unstructured OCR text based on a provided schema
    or document type hints.

    Args:
        text: OCR-normalized document text
        field_schema: Optional dictionary defining expected fields and types
        document_type: Type of document (invoice, form, receipt, etc.)
        model_id: Bedrock model identifier

    Returns:
        FieldExtractionResponse with extracted structured fields
    """
    client = create_bedrock_runtime_client()

    prompt = _build_extraction_prompt(text, field_schema, document_type)

    # Build Claude 3 message format for Amazon Bedrock
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.1,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    content_blocks = result.get("content", [])

    # Extract JSON from Claude's response
    extracted_json = _parse_json_from_response(content_blocks)

    fields = _normalize_to_fields(extracted_json, field_schema)
    overall_confidence = _calculate_overall_confidence(fields)

    return FieldExtractionResponse(
        fields=fields,
        document_type=document_type,
        confidence=overall_confidence,
    )


def extract_invoice_fields(text: str, model_id: str = BEDROCK_MODEL_ID) -> FieldExtractionResponse:
    """
    Extract invoice-specific fields using Amazon Bedrock Claude.

    Args:
        text: OCR text from an invoice document
        model_id: Bedrock model identifier

    Returns:
        FieldExtractionResponse with invoice fields
    """
    invoice_schema = {
        "fields": {
            "invoice_number": {"type": "string", "description": "Invoice number or ID"},
            "invoice_date": {"type": "date", "description": "Invoice date"},
            "due_date": {"type": "date", "description": "Payment due date"},
            "vendor_name": {"type": "string", "description": "Vendor or company name"},
            "vendor_address": {"type": "string", "description": "Vendor address"},
            "total_amount": {"type": "number", "description": "Total invoice amount"},
            "subtotal": {"type": "number", "description": "Subtotal before tax"},
            "tax_amount": {"type": "number", "description": "Tax amount"},
            "currency": {"type": "string", "description": "Currency code"},
            "line_items": {"type": "array", "description": "List of line items"},
        }
    }

    return extract_fields_from_text(text, invoice_schema, "invoice", model_id)


def extract_receipt_fields(text: str, model_id: str = BEDROCK_MODEL_ID) -> FieldExtractionResponse:
    """
    Extract receipt-specific fields using Amazon Bedrock Claude.

    Args:
        text: OCR text from a receipt document
        model_id: Bedrock model identifier

    Returns:
        FieldExtractionResponse with receipt fields
    """
    receipt_schema = {
        "fields": {
            "merchant_name": {"type": "string", "description": "Merchant or store name"},
            "transaction_date": {"type": "date", "description": "Date of transaction"},
            "transaction_time": {"type": "string", "description": "Time of transaction"},
            "total": {"type": "number", "description": "Total amount"},
            "subtotal": {"type": "number", "description": "Subtotal"},
            "tax": {"type": "number", "description": "Tax amount"},
            "payment_method": {"type": "string", "description": "Payment method used"},
            "receipt_number": {"type": "string", "description": "Receipt or transaction number"},
        }
    }

    return extract_fields_from_text(text, receipt_schema, "receipt", model_id)


def _build_extraction_prompt(text: str, schema: Optional[dict], doc_type: str) -> str:
    """
    Build the extraction prompt for Claude.

    Args:
        text: Document text to extract from
        schema: Field schema definition
        doc_type: Document type identifier

    Returns:
        Prompt string for Claude model
    """
    schema_section = ""
    if schema and "fields" in schema:
        schema_section = "Extract the following fields from the document:\n"
        for field_name, field_info in schema["fields"].items():
            desc = field_info.get("description", "")
            ftype = field_info.get("type", "string")
            schema_section += f"- {field_name} ({ftype}): {desc}\n"
    else:
        schema_section = f"Extract all relevant fields from this {doc_type} document. "
        schema_section += "Identify key information such as dates, amounts, names, addresses, "
        schema_section += "identifiers, and any other structured data present."

    prompt = f"""You are a document data extraction assistant. Analyze the following document text and extract structured fields as JSON.

{schema_section}

IMPORTANT:
- Return ONLY a valid JSON object with the extracted field names as keys and their values.
- Use null for fields that cannot be found in the document.
- For dates, use ISO 8601 format (YYYY-MM-DD).
- For numbers, return numeric values without currency symbols.
- Include a "_confidence" key with a value between 0 and 1 representing your overall confidence.

Document text:
---
{text}
---
"""
    return prompt


def _parse_json_from_response(content_blocks: list) -> dict:
    """
    Parse JSON from Claude's response content blocks.

    Args:
        content_blocks: List of content blocks from Claude response

    Returns:
        Parsed JSON dictionary
    """
    for block in content_blocks:
        if block.get("type") == "text":
            text = block.get("text", "")
            # Handle markdown code block wrapping
            if "```json" in text:
                start = text.index("```json") + 7
                end = text.index("```", start)
                text = text[start:end].strip()
            elif "```" in text:
                start = text.index("```") + 3
                end = text.index("```", start)
                text = text[start:end].strip()

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue

    return {}


def _normalize_to_fields(extracted: dict, schema: Optional[dict] = None) -> List[ExtractedField]:
    """
    Normalize extracted JSON to ExtractedField objects.

    Args:
        extracted: Dictionary of extracted fields
        schema: Optional field schema

    Returns:
        List of ExtractedField objects
    """
    fields = []
    for key, value in extracted.items():
        if key == "_confidence":
            continue

        if isinstance(value, (list, dict)):
            value = json.dumps(value)

        field = ExtractedField(
            field_name=key,
            value=str(value) if value is not None else "",
            confidence=extracted.get("_confidence", 0.0),
            field_type=_infer_field_type(value),
        )
        fields.append(field)

    return fields


def _infer_field_type(value) -> str:
    """
    Infer the type of an extracted field value.

    Args:
        value: Field value

    Returns:
        Type string
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, (list, dict)):
        return "object"
    return "string"


def _calculate_overall_confidence(fields: List[ExtractedField]) -> float:
    """
    Calculate overall confidence from extracted fields.

    Args:
        fields: List of ExtractedField objects

    Returns:
        Average confidence score
    """
    if not fields:
        return 0.0
    scores = [f.confidence for f in fields if f.confidence > 0]
    return sum(scores) / len(scores) if scores else 0.5


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python document_field_extraction.py <text_file> [document_type]")
        sys.exit(1)

    text_file = sys.argv[1]
    doc_type = sys.argv[2] if len(sys.argv) > 2 else "general"

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    result = extract_fields_from_text(text, document_type=doc_type)
    print(f"Extracted {len(result.fields)} fields (confidence: {result.confidence:.1%}):")
    for field in result.fields:
        print(f"  {field.field_name}: {field.value}")

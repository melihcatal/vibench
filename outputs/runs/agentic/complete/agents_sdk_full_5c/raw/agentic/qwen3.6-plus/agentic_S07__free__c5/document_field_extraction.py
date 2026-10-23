"""
Extract structured fields from OCR-normalized document text using OpenAI GPT.

Uses the OpenAI Chat Completions API with gpt-4o-mini to extract structured
fields from OCR-normalized document text using JSON schema-guided extraction.
"""

import os
import json
from typing import Optional, Dict, Any, List

import openai


# OpenAI API configuration
OPENAI_API_HOST = "api.openai.com"
OPENAI_CHAT_MODEL = "gpt-4o-mini"


FIELD_EXTRACTION_SYSTEM_PROMPT = """\
You are a document field extraction assistant. Extract structured fields \
from the provided OCR-normalized document text. Return ONLY valid JSON \
matching the requested schema. Do not include any explanation or markdown.
"""


def extract_structured_fields(
    document_text: str,
    field_schema: Dict[str, Any],
    model: str = OPENAI_CHAT_MODEL,
    api_key: Optional[str] = None,
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-normalized document text.
    
    This function uses the OpenAI Chat Completions API with the gpt-4o-mini
    model to extract structured fields from document text based on a
    JSON schema definition.
    
    Args:
        document_text: OCR-normalized document text.
        field_schema: JSON schema defining the fields to extract.
        model: OpenAI model to use (default: gpt-4o-mini).
        api_key: OpenAI API key (uses OPENAI_API_KEY env var if None).
        temperature: Sampling temperature (0.0 for deterministic output).
        
    Returns:
        Dict[str, Any]: Extracted fields matching the schema.
        
    Raises:
        ValueError: If document_text is empty or schema is invalid.
        openai.APIError: If OpenAI API call fails.
    """
    if not document_text or not document_text.strip():
        raise ValueError("Document text cannot be empty")
    
    if not field_schema:
        raise ValueError("Field schema cannot be empty")
    
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )
    
    schema_description = json.dumps(field_schema, indent=2)
    
    user_prompt = (
        f"Extract the following fields from the document text:\n\n"
        f"Schema:\n{schema_description}\n\n"
        f"Document text:\n{document_text}"
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": FIELD_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    
    response_text = response.choices[0].message.content
    
    try:
        extracted_fields = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}") from e
    
    return extracted_fields


def extract_invoice_fields(
    document_text: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract invoice-specific fields from OCR text.
    
    Args:
        document_text: OCR-normalized document text.
        api_key: OpenAI API key.
        
    Returns:
        Dict[str, Any]: Extracted invoice fields.
    """
    invoice_schema = {
        "invoice_number": "string",
        "invoice_date": "string",
        "due_date": "string",
        "vendor_name": "string",
        "vendor_address": "string",
        "total_amount": "number",
        "tax_amount": "number",
        "currency": "string",
        "line_items": [
            {
                "description": "string",
                "quantity": "number",
                "unit_price": "number",
                "amount": "number",
            }
        ],
    }
    
    return extract_structured_fields(
        document_text=document_text,
        field_schema=invoice_schema,
        api_key=api_key,
    )


def extract_receipt_fields(
    document_text: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract receipt-specific fields from OCR text.
    
    Args:
        document_text: OCR-normalized document text.
        api_key: OpenAI API key.
        
    Returns:
        Dict[str, Any]: Extracted receipt fields.
    """
    receipt_schema = {
        "merchant_name": "string",
        "merchant_address": "string",
        "transaction_date": "string",
        "transaction_time": "string",
        "receipt_number": "string",
        "items": [
            {
                "item_name": "string",
                "price": "number",
            }
        ],
        "subtotal": "number",
        "tax": "number",
        "total": "number",
        "payment_method": "string",
    }
    
    return extract_structured_fields(
        document_text=document_text,
        field_schema=receipt_schema,
        api_key=api_key,
    )


def extract_id_fields(
    document_text: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract ID document fields from OCR text.
    
    Args:
        document_text: OCR-normalized document text.
        api_key: OpenAI API key.
        
    Returns:
        Dict[str, Any]: Extracted ID document fields.
    """
    id_schema = {
        "document_type": "string",
        "full_name": "string",
        "date_of_birth": "string",
        "document_number": "string",
        "expiry_date": "string",
        "issue_date": "string",
        "issuing_authority": "string",
        "address": "string",
    }
    
    return extract_structured_fields(
        document_text=document_text,
        field_schema=id_schema,
        api_key=api_key,
    )


def extract_fields_from_blocks(
    text_blocks: List[Dict[str, str]],
    field_schema: Dict[str, Any],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured fields from a list of OCR text blocks.
    
    Args:
        text_blocks: List of dicts with 'text' key for each block.
        field_schema: JSON schema defining the fields to extract.
        api_key: OpenAI API key.
        
    Returns:
        Dict[str, Any]: Extracted fields.
    """
    combined_text = "\n".join(block.get("text", "") for block in text_blocks)
    return extract_structured_fields(
        document_text=combined_text,
        field_schema=field_schema,
        api_key=api_key,
    )

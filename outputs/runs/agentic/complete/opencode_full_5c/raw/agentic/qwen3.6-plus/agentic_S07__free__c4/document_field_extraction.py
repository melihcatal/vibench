import os
import json
from typing import Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL_ID = "gpt-4o"


def extract_structured_fields(
    document_text: str,
    field_schema: dict,
    temperature: float = 0.0,
) -> dict:
    system_prompt = (
        "You are a document field extraction assistant. Extract structured fields from the provided document text "
        "according to the given JSON schema. Return only valid JSON matching the schema. "
        "If a field cannot be found, set its value to null."
    )
    user_prompt = (
        f"Extract the following fields from this document text:\n\n"
        f"Document text:\n{document_text}\n\n"
        f"Field schema:\n{json.dumps(field_schema, indent=2)}"
    )
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_CHAT_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    try:
        extracted_fields = json.loads(content)
    except json.JSONDecodeError:
        extracted_fields = {}
    return {
        "fields": extracted_fields,
        "model": OPENAI_MODEL_ID,
        "usage": data.get("usage", {}),
    }


def extract_form_fields(
    document_text: str,
    field_names: list,
    temperature: float = 0.0,
) -> dict:
    field_schema = {
        "type": "object",
        "properties": {name: {"type": "string"} for name in field_names},
        "required": [],
    }
    return extract_structured_fields(
        document_text=document_text,
        field_schema=field_schema,
        temperature=temperature,
    )


def extract_invoice_fields(
    document_text: str,
    temperature: float = 0.0,
) -> dict:
    field_schema = {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string"},
            "invoice_date": {"type": "string"},
            "due_date": {"type": "string"},
            "vendor_name": {"type": "string"},
            "vendor_address": {"type": "string"},
            "customer_name": {"type": "string"},
            "customer_address": {"type": "string"},
            "subtotal": {"type": "string"},
            "tax": {"type": "string"},
            "total": {"type": "string"},
            "currency": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "string"},
                        "unit_price": {"type": "string"},
                        "amount": {"type": "string"},
                    },
                },
            },
        },
        "required": [],
    }
    return extract_structured_fields(
        document_text=document_text,
        field_schema=field_schema,
        temperature=temperature,
    )


def extract_id_document_fields(
    document_text: str,
    temperature: float = 0.0,
) -> dict:
    field_schema = {
        "type": "object",
        "properties": {
            "document_type": {"type": "string"},
            "full_name": {"type": "string"},
            "date_of_birth": {"type": "string"},
            "document_number": {"type": "string"},
            "expiry_date": {"type": "string"},
            "issuing_country": {"type": "string"},
            "address": {"type": "string"},
            "gender": {"type": "string"},
        },
        "required": [],
    }
    return extract_structured_fields(
        document_text=document_text,
        field_schema=field_schema,
        temperature=temperature,
    )

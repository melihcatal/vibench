import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from openai import OpenAI


def normalize_expense_fields(
    extracted_data: Dict[str, Any], document_type: str = "invoice"
) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema using OpenAI GPT-4.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    schema = {
        "type": "object",
        "properties": {
            "vendor": {"type": "string"},
            "merchant": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "total_amount": {"type": "number"},
            "tax_amount": {"type": "number"},
            "currency": {"type": "string", "default": "USD"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "amount": {"type": "number"},
                    },
                },
            },
            "confidence": {"type": "number"},
            "document_type": {"type": "string"},
        },
        "required": ["total_amount", "document_type"],
    }

    prompt = f"""
    Normalize the following extracted {document_type} data into the standard expense schema.
    Extract and transform fields as needed:
    
    Extracted data: {json.dumps(extracted_data, indent=2)}
    
    Schema: {json.dumps(schema, indent=2)}
    
    Return ONLY a valid JSON object that matches the schema. Include all available fields.
    For dates, format as YYYY-MM-DD.
    For amounts, ensure they are numbers.
    If currency is not specified, default to "USD".
    Add a confidence score between 0 and 1 based on data completeness.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a data normalization assistant. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    normalized_data = json.loads(response.choices[0].message.content)

    normalized_data["normalized_at"] = datetime.utcnow().isoformat()
    normalized_data["source_provider"] = "openai_gpt4"

    return normalized_data

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def extract_invoice_fields(invoice_text: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_MODEL", "openai/gpt-5.4-mini")
    schema = {
        "name": "invoice_fields",
        "schema": {
            "type": "object",
            "properties": {
                "vendor": {"type": ["string", "null"]},
                "date": {"type": ["string", "null"]},
                "total": {"type": ["number", "string", "null"]},
                "line_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": ["string", "null"]},
                            "quantity": {"type": ["number", "string", "null"]},
                            "unit_price": {"type": ["number", "string", "null"]},
                            "amount": {"type": ["number", "string", "null"]},
                        },
                        "required": ["description", "quantity", "unit_price", "amount"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["vendor", "date", "total", "line_items"],
            "additionalProperties": False,
        },
        "strict": True,
    }
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Extract invoice vendor, date, total, and line-item fields as structured JSON.",
            },
            {"role": "user", "content": invoice_text},
        ],
        text={"format": {"type": "json_schema", "json_schema": schema}},
    )
    return response.output_parsed  # type: ignore[attr-defined]


def extract_invoice_fields_from_text(invoice_text: str) -> Dict[str, Any]:
    return extract_invoice_fields(invoice_text)

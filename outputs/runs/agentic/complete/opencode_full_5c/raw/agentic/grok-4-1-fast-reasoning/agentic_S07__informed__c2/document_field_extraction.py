import os
import json
import openai
from typing import Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def document_field_extraction(document_text: str) -> Dict[str, Any]:
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "invoice",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "vendor_name": {"type": "string"},
                    "invoice_number": {"type": "string"},
                    "invoice_date": {"type": "string"},
                    "due_date": {"type": "string"},
                    "total_amount": {"type": "number"},
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
                },
                "required": ["vendor_name", "total_amount"],
                "additionalProperties": False,
            },
        },
    }
    messages = [
        {
            "role": "user",
            "content": f"Extract structured invoice fields from this OCR text as JSON:\n\n{document_text}",
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format=response_format,
        temperature=0,
    )
    content = response.choices[0].message.content
    return json.loads(content)

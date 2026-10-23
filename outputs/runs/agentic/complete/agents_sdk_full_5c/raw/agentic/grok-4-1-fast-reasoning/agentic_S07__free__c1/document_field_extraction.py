import openai
import os
import json
from typing import Dict, Any

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def document_field_extraction(text: str, fields_schema: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-normalized document text.
    """
    if fields_schema is None:
        fields_schema = {
            "type": "object",
            "properties": {
                "invoice_number": {"type": "string"},
                "date": {"type": "string"},
                "total": {"type": "number"},
            },
            "required": ["invoice_number", "date", "total"]
        }
    
    messages = [
        {
            "role": "user",
            "content": f"""Extract the following fields as JSON from the document text.

Document text:
{text}

JSON Schema:
{json.dumps(fields_schema)}"""
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )
    
    extracted = json.loads(response.choices[0].message.content)
    return extracted

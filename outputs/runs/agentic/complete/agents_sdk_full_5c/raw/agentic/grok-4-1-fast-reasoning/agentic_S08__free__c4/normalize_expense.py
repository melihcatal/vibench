from openai import OpenAI
import os
import json
from typing import Dict, Any

def normalize_expense(extracted_fields: Dict[str, Any], document_type: str = "invoice") -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""Normalize the following extracted {document_type} fields into a standard JSON schema.

Extracted data: {json.dumps(extracted_fields, indent=2)}

Standard output JSON:
{{
  "document_type": "{document_type}",
  "vendor_merchant": "str",
  "date": "YYYY-MM-DD or similar",
  "tax": float|null,
  "total": float,
  "line_items": [{{"description": "str", "quantity": int|null, "amount": float}}],
  "confidence": {{"avg": float}}
}}

Respond with ONLY the JSON object."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    
    normalized_json = response.choices[0].message.content
    return json.loads(normalized_json)
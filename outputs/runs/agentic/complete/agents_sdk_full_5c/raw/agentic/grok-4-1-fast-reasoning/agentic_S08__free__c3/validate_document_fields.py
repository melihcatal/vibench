import os
import json
from anthropic import Anthropic
from typing import Dict, Any
from document_models import ValidationResult

def validate_document_fields(fields: Dict[str, Any]) -> ValidationResult:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f'''Validate these extracted document fields. Required: vendor/merchant, date, total, line_items/items. Each field value non-empty, confidence > 0.7.

Fields: {json.dumps(fields)}

Compute avg_confidence (mean of all confidences).

JSON output only:
{{
  "is_valid": true|false,
  "avg_confidence": 0.85,
  "missing_fields": ["vendor"],
  "low_confidence_fields": ["date"]
}}'''

    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=500,
        messages=[{'role': 'user', 'content': prompt}]
    )
    result_text = message.content[0].text.strip()
    return json.loads(result_text)
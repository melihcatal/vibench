import os
import json
from anthropic import Anthropic
from typing import Dict, Any
from document_models import ValidationResult

def validate_document_fields(fields: Dict[str, Any], doc_type: str = 'invoice') -> Dict[str, Any]:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    required_fields = ['vendor_or_merchant' if doc_type == 'receipt' else 'vendor', 'date', 'total']
    prompt = f"""Validate these {doc_type} fields: {json.dumps(fields)}.

Required: {required_fields}.
Check completeness, data types, reasonableness (e.g. total > 0).
Output ONLY JSON: {{"is_valid": bool, "missing_fields": [str], "issues": [str], "overall_confidence": 0.0-1.0}}"""

    message = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=400,
        messages=[{'role': 'user', 'content': prompt}]
    )
    validation_data = json.loads(message.content[0].text)
    return ValidationResult(**validation_data).model_dump()
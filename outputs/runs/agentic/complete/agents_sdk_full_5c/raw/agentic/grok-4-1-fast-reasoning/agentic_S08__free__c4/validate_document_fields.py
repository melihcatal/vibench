from anthropic import Anthropic
import os
import json
import re
from typing import Dict, Any

def validate_document_fields(fields: Dict[str, Any], document_type: str = "invoice") -> Dict[str, Any]:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    prompt = f"""Validate the extracted {document_type} document fields for completeness, accuracy, and consistency.

Fields: {json.dumps(fields)}

Validation criteria:
- Required: vendor/merchant, total > 0, date present
- Confidences mostly > 0.7
- Total reasonable

Output ONLY JSON:
{{
  "valid": true|false,
  "issues": ["list of issues or []"],
  "overall_confidence": 0.0-1.0
}}"""
    
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = message.content[0].text.strip()
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        validation = json.loads(json_match.group())
    else:
        validation = {"valid": False, "issues": ["Parse error"], "overall_confidence": 0.0}
    
    return validation
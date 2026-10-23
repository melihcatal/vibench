import os
import json
from anthropic import Anthropic
from document_client import validate_env
from document_models import ValidationResult
from typing import Dict, Any, List

validate_env("anthropic")


def validate_document_fields(extracted_data: Dict[str, Any]) -> ValidationResult:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Validate extracted fields: {json.dumps(extracted_data, default=str)}

Required: vendor/merchant, date, total present and non-empty.
Date valid YYYY-MM-DD like.
Total > 0.
Line items at least 1.
All confidences >=0.7, avg >=0.8.

Return ONLY JSON: {{"valid": bool, "issues": [str,...], "avg_confidence": float, "min_confidence": float}}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    val_dict = json.loads(message.content[0].text)
    return ValidationResult(**val_dict)

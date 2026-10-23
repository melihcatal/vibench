import os
import json
import google.generativeai as genai
from typing import Dict, Any, Union
from document_models import ValidationResult, NormalizedExpense, ExtractedInvoice, ExtractedReceipt

def validate_document_fields(fields: Union[ExtractedInvoice, ExtractedReceipt, NormalizedExpense]) -> ValidationResult:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Validate these document fields for completeness, consistency (e.g. total positive, date valid), and confidence > 0.7.
Required: entity_name/vendor/merchant, date, total, items.
Output ONLY JSON: {{"is_valid": bool, "issues": ["str", ...], "overall_confidence": float(0-1)}}

Fields: {json.dumps(fields)}"""
    response = model.generate_content(prompt)
    validated_str = response.text.strip()
    # Assume response is clean JSON
    validated = json.loads(validated_str)
    return ValidationResult(**validated)

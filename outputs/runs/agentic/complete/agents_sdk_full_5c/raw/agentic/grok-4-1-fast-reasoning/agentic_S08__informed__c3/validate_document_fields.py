import os
import json
import google.generativeai as genai
from typing import Dict, Any
from document_models import NormalizedExpense

def validate_document_fields(normalized: NormalizedExpense) -> Dict[str, Any]:
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config=genai.types.GenerationConfig(
            response_mime_type='application/json',
            temperature=0.1
        )
    )
    prompt = f"""Validate this normalized expense record:
{json.dumps(normalized, indent=2)}

Check:
- All required fields present: type, vendor_or_merchant, date, total, line_items
- date is valid YYYY-MM-DD
- total > 0
- line_items non-empty, amounts >0
- No obvious errors

Return ONLY JSON:
{{
  "valid": boolean,
  "issues": ["list of issues or empty"],
  "overall_confidence": number 0-1
}}"""
    response = model.generate_content(prompt)
    validation = json.loads(response.text)
    return validation

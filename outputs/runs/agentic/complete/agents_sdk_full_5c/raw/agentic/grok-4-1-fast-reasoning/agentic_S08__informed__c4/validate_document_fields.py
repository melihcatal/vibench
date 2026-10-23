import google.generativeai as genai
import os
import json
from document_models import NormalizedExpense

def validate_document_fields(fields: dict) -> dict:
    try:
        NormalizedExpense(**fields)
        schema_valid = True
    except ValueError as e:
        return {"valid": False, "schema_errors": str(e), "semantic_valid": False}
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return {"valid": schema_valid, "error": "Missing GOOGLE_API_KEY"}
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Validate the following normalized expense record:

{json.dumps(fields, indent=2)}

Checks:
1. transaction_date is plausible ISO or YYYY-MM-DD
2. total_amount > 0
3. sum(line_items.amount) + tax_amount ≈ total_amount (within 5%)
4. merchant_name not empty
5. Confidences high if present

Respond ONLY with valid JSON:
{{"valid": boolean, "issues": ["list of issues"], "overall_confidence": number 0-1}}"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3].strip()
        elif text.startswith('```'):
            text = text[3:-3].strip()
        val_dict = json.loads(text)
        val_dict["schema_valid"] = schema_valid
        val_dict["overall_valid"] = schema_valid and val_dict.get("valid", False)
        return val_dict
    except Exception as e:
        return {"valid": schema_valid, "error": str(e)}
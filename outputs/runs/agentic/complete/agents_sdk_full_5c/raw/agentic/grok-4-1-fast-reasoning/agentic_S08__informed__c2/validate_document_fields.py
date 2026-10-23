import os
import google.generativeai as genai
import json
import re
from document_models import NormalizedExpense
from typing import Dict, Any

def validate_document_fields(normalized: NormalizedExpense) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Set GOOGLE_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""Validate expense: {json.dumps(normalized, indent=2)}.
Check required fields, total > 0, date format, items sum ~ total.

Output ONLY JSON: {{"valid": true/false, "issues": ["list"], "avg_confidence": float}}"""

    response = model.generate_content(prompt)
    content = response.text.strip()

    json_match = re.search(r'\\{[^}]+\\}', content, re.DOTALL)
    if json_match:
        validation = json.loads(json_match.group())
    else:
        validation = {"valid": False, "issues": ["Parse error"], "avg_confidence": 0.0}

    return validation
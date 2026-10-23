import os
import json
import google.generativeai as genai
from typing import Union
from document_models import DocumentFields, NormalizedExpense

def validate_document_fields(data: Union[DocumentFields, NormalizedExpense], min_confidence: float = 0.8) -> dict:
    issues = []
    
    # Local structural validation
    if isinstance(data, DocumentFields):
        conf = data.confidence
        if not data.vendor:
            issues.append("Missing vendor/merchant")
        elif conf.get('vendor', 0) < min_confidence:
            issues.append(f"Low confidence for vendor: {conf.get('vendor')}")
        if not data.total:
            issues.append("Missing total")
        elif data.total <= 0:
            issues.append("Invalid total amount")
    
    # LLM semantic validation
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    data_str = json.dumps(data.model_dump() if hasattr(data, 'model_dump') else data.__dict__)
    prompt = f"""Validate this expense document fields:
- Required fields present?
- Date format valid?
- Total > 0?
- Line items sum approximates total?
- Any anomalies?

Output JSON: {{"valid": bool, "issues": ["list of issues"]}}

Data: {data_str}"""
    
    response = model.generate_content(prompt)
    llm_text = response.text
    
    # Simple parse, assume starts with {"valid"
    try:
        llm_json_start = llm_text.find('{')
        llm_json = json.loads(llm_text[llm_json_start:])
        issues.extend(llm_json.get('issues', []))
    except:
        pass  # fallback to local
    
    return {"valid": len(issues) == 0, "issues": issues}
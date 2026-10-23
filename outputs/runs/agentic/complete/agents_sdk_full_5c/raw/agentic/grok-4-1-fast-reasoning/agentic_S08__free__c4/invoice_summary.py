import google.generativeai as genai
import os
import json
from typing import Dict, Any

def invoice_summary(extracted_fields: Dict[str, Any]) -> str:
    api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""Summarize this invoice in 1-2 sentences for quick review.

Details: {json.dumps(extracted_fields)}

Keep factual and concise."""
    
    response = model.generate_content(prompt)
    return response.text.strip()
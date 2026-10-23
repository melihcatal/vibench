import os
import google.generativeai as genai
import json
from typing import Dict, Any


def generate_invoice_summary(invoice_fields: Dict[str, Any]) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""Provide a concise summary of this invoice in 2-3 sentences:
{json.dumps(invoice_fields)}"""

    response = model.generate_content(prompt)
    return response.text

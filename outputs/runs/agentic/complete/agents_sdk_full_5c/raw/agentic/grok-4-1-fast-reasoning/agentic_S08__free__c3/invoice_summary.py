import os
import google.generativeai as genai
from document_models import InvoiceFields
from typing import Dict, Any

def invoice_summary(fields: InvoiceFields) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_GENERATIVE_AI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f'''Create a concise human-readable summary of this invoice:

{fields}'''
    response = model.generate_content(prompt)
    return response.text
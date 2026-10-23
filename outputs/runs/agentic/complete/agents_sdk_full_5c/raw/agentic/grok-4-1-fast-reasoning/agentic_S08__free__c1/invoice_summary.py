import os
from openai import OpenAI
from document_models import ExtractedInvoice
from typing import Dict, Any

def invoice_summary(extracted: Dict[str, Any]) -> str:
    client = OpenAI(
        api_key=os.getenv('XAI_API_KEY'),
        base_url="https://api.x.ai/v1"
    )
    prompt = f"""Provide a concise human-readable summary of this invoice extraction:

{extracted}

Include vendor, date, total, and key line items."""
    response = client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

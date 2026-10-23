import os
import json
from typing import Dict, Any
from anthropic import Anthropic
from document_models import InvoiceExtract

def invoice_summary(invoice_fields: InvoiceExtract) -> str:
    client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    prompt = f"""Provide a concise human-readable summary of this invoice extraction:
{json.dumps(invoice_fields, indent=2, default=str)}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

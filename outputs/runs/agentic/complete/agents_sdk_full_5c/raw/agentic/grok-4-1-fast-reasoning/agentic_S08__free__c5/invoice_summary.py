import os
from anthropic import Anthropic
from typing import Dict, Any
from document_models import InvoiceFields

def invoice_summary(invoice_fields: Dict[str, Any]) -> str:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    invoice = InvoiceFields(**invoice_fields)
    prompt = f"""Provide a concise human-readable summary of this invoice.

Vendor: {invoice.vendor}
Date: {invoice.date}
Total: ${invoice.total:.2f}
Line items: {len(invoice.line_items)} items totaling ${sum(item.total or 0 for item in invoice.line_items):.2f}"""

    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=250,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return message.content[0].text
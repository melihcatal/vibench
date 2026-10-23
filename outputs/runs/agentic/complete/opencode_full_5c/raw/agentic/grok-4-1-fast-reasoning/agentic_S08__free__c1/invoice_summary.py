import os
from openai import OpenAI
from document_models import InvoiceExtract


def invoice_summary(extract: InvoiceExtract) -> str:
    client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
    if not os.getenv("XAI_API_KEY"):
        raise ValueError("XAI_API_KEY not set")
    prompt = f"""Provide a concise business summary of this invoice (2-3 sentences):

- Vendor: {extract.vendor.content}
- Date: {extract.invoice_date.content}
- Total: ${extract.total_amount.content}
- {len(extract.line_items)} line items"""
    response = client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

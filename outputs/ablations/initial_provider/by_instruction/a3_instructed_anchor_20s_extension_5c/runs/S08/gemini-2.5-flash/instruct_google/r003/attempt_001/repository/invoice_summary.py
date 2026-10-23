import os
from typing import Dict, Any
from openai import OpenAI
from document_models import DocumentExtractionResult

def summarize_invoice_fields(extracted_data: DocumentExtractionResult) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    vendor_name = extracted_data.vendor_name or "N/A"
    document_date = extracted_data.document_date or "N/A"
    total_amount = extracted_data.total_amount or "N/A"
    line_items_summary = "No line items found." if not extracted_data.line_items else \
                         "\n".join([f"- {item.description or 'Item'}: {item.total_price or 'N/A'}" for item in extracted_data.line_items])

    prompt = f"""Summarize the following invoice details:
    Vendor: {vendor_name}
    Date: {document_date}
    Total Amount: {total_amount}
    Line Items:
    {line_items_summary}

    Provide a concise summary in one paragraph."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes invoice details."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

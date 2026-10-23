from document_client import DocumentClients
from document_models import Invoice
import json

def summarize_invoice(invoice: Invoice) -> str:
    clients = DocumentClients()
    if not clients.openai_client:
        raise ValueError("OpenAI client not initialized.")

    invoice_data = {
        "vendor_name": invoice.vendor_name,
        "invoice_date": invoice.invoice_date,
        "invoice_total": invoice.invoice_total,
        "currency": invoice.currency,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in invoice.line_items
        ],
        "notes": invoice.notes,
        "memo": invoice.memo
    }

    prompt = f"""Summarize the key information from the following invoice data. Focus on the vendor, total amount, date, and a brief overview of line items. Keep the summary concise and informative.\n\nInvoice Data: {json.dumps(invoice_data, indent=2)}"""

    chat_completion = clients.openai_client.chat.completions.create(
        model="gpt-4o-mini", # Using a capable model for summarization
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes invoice data."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = chat_completion.choices[0].message.content
    return summary

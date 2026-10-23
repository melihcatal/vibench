import os
import anthropic
from document_models import InvoiceExtraction


def summarize_invoice(invoice: InvoiceExtraction) -> dict:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    line_items_summary = ""
    for item in invoice.line_items:
        line_items_summary += f"- {item.description}: {item.quantity} x {item.unit_price} = {item.amount}\n"

    prompt = f"""Summarize the following invoice data in JSON format:
{{
  "vendor": "{invoice.vendor_name}",
  "invoice_number": "{invoice.invoice_number}",
  "invoice_date": "{invoice.invoice_date}",
  "total_amount": {invoice.total_amount},
  "tax_amount": {invoice.tax_amount},
  "currency": "{invoice.currency}",
  "line_item_count": {len(invoice.line_items)},
  "line_items_summary": "{line_items_summary.strip()}",
  "summary_text": "Brief human-readable summary of the invoice"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are an invoice summarization assistant. Return ONLY valid JSON.",
        messages=[{"role": "user", "content": prompt}],
    )

    import json

    content = message.content[0].text
    summary_data = json.loads(content)

    return {
        "vendor": summary_data.get("vendor", invoice.vendor_name),
        "invoice_number": summary_data.get("invoice_number", invoice.invoice_number),
        "invoice_date": summary_data.get("invoice_date", invoice.invoice_date),
        "total_amount": summary_data.get("total_amount", invoice.total_amount),
        "tax_amount": summary_data.get("tax_amount", invoice.tax_amount),
        "currency": summary_data.get("currency", invoice.currency),
        "line_item_count": summary_data.get("line_item_count", len(invoice.line_items)),
        "line_items_summary": summary_data.get("line_items_summary", ""),
        "summary_text": summary_data.get("summary_text", ""),
        "model": "claude-sonnet-4-20250514",
        "provider": "anthropic",
    }

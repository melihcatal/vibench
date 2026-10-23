import os
import google.generativeai as genai
from document_models import InvoiceFields


def summarize_invoice(invoice_fields: InvoiceFields) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following invoice details:\n"
    prompt += f"Vendor Name: {invoice_fields.vendor_name}\n"
    prompt += f"Invoice Date: {invoice_fields.invoice_date}\n"
    prompt += f"Invoice Total: {invoice_fields.invoice_total}\n"
    if invoice_fields.line_items:
        prompt += "Line Items:\n"
        for item in invoice_fields.line_items:
            prompt += f"- Description: {item.description}, Quantity: {item.quantity}, Unit Price: {item.unit_price}, Amount: {item.amount}\n"

    response = model.generate_content(prompt)
    return response.text

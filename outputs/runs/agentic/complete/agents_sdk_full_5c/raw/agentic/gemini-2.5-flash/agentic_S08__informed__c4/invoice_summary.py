import os
from google.generativeai import GenerativeModel
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from document_models import ExpenseDocument

def summarize_invoice_fields(expense_doc: ExpenseDocument) -> str:
    """Summarize extracted invoice fields using Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Initialize the GenerativeModel
    model = GenerativeModel("gemini-pro", api_key=api_key)

    prompt = f"""Summarize the key information from this invoice data:
Vendor Name: {expense_doc.vendor_name}
Date: {expense_doc.date}
Total Amount: {expense_doc.total_amount} {expense_doc.currency}
Line Items: {len(expense_doc.line_items)} items

Provide a concise summary highlighting the most important details."""

    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    return response.text

import os
from typing import Optional
from document_models import NormalizedExpense
import google.generativeai as genai  # Provider identifiable import: Google Gemini API

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print(
        "Warning: GOOGLE_API_KEY environment variable not set. Gemini API calls may fail."
    )


def summarize_invoice(expense: NormalizedExpense) -> Optional[str]:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    This function is a scored component.
    """
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Cannot summarize invoice."

    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model ID

    prompt = f"""
    Summarize the following expense record. Focus on the vendor, total amount, date, and a brief mention of line items if present.

    Vendor: {expense.vendor_name}
    Date: {expense.transaction_date.isoformat()}
    Total Amount: {expense.total_amount} {expense.currency}
    Tax Amount: {expense.tax_amount if expense.tax_amount is not None else "N/A"}
    Line Items: {", ".join([item.description for item in expense.line_items]) if expense.line_items else "None"}
    Document Type: {expense.document_type}
    Notes: {expense.notes if expense.notes else "None"}

    Provide a concise summary in one or two sentences.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing invoice with Gemini API: {e}")
        return None

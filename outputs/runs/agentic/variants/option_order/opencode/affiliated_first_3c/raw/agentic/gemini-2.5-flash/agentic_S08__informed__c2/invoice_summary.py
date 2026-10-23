import os
import google.generativeai as genai
from document_models import NormalizedExpense


def summarize_invoice_fields(expense: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following expense record in a concise paragraph, highlighting the key details:

Document Type: {expense.document_type}
Vendor/Merchant: {expense.vendor_or_merchant_name}
Date: {expense.transaction_date}
Total Amount: {expense.total_amount} {expense.currency}
Tax Amount: {expense.tax_amount if expense.tax_amount is not None else "N/A"}
Line Items: {"; ".join([f"{item.description} (Qty: {item.quantity}, Price: {item.total_price})" for item in expense.line_items]) if expense.line_items else "N/A"}
Notes: {expense.notes if expense.notes else "N/A"}

Summary:"""

    response = model.generate_content(prompt)
    return response.text

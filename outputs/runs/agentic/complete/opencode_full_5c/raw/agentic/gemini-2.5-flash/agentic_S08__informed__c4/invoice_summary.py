from typing import Dict, Any
from document_client import get_google_gemini_client
from document_models import NormalizedExpense


def summarize_invoice_fields(expense_record: NormalizedExpense) -> str:
    model = get_google_gemini_client()

    prompt = f"""Summarize the following expense record in a concise manner, highlighting the vendor, total amount, and key line items:
    Vendor: {expense_record.vendor_name}
    Date: {expense_record.transaction_date}
    Total Amount: {expense_record.total_amount} {expense_record.currency}
    Line Items: {", ".join([f"{item.description} ({item.total_price})" for item in expense_record.line_items])}
    """

    response = model.generate_content(prompt)
    return response.text

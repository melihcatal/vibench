from document_client import DocumentClient
from document_models import NormalizedExpense


def summarize_invoice(expense: NormalizedExpense) -> str:
    client = DocumentClient()
    model = client.gemini_model

    # Construct a prompt for summarizing the invoice
    summary_prompt = f"""Summarize the following expense record. Focus on the key details like vendor, total amount, date, and main line items. Keep it concise. Ignore if field is not provided. Example: Invoice from ExampleVendor for $100.00 on 2023-01-15, including item1 and item2.

    Document Type: {expense.document_type}
    Vendor/Merchant: {expense.vendor_merchant_name}
    Transaction Date: {expense.transaction_date}
    Total Amount: {expense.total_amount} {expense.currency}
    Tax Amount: {expense.tax_amount}
    Line Items:
    """
    for item in expense.line_items:
        summary_prompt += f"    - {item.description} (Quantity: {item.quantity}, Unit Price: {item.unit_price}, Total Price: {item.total_price})\n"

    if expense.notes:
        summary_prompt += f"    Notes: {expense.notes}\n"

    response = model.generate_content(summary_prompt)
    return response.text

import os
import google.generativeai as genai
from document_models import NormalizedExpense

def summarize_invoice(expense: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the key information from the following expense record.
    Focus on the vendor, total amount, date, and a brief overview of line items if present.
    
    Document Type: {expense.document_type}
    Vendor: {expense.vendor_name if expense.vendor_name else 'N/A'}
    Date: {expense.transaction_date if expense.transaction_date else 'N/A'}
    Total Amount: {expense.total_amount if expense.total_amount is not None else 'N/A'} {expense.currency if expense.currency else ''}
    Tax Amount: {expense.tax_amount if expense.tax_amount is not None else 'N/A'} {expense.currency if expense.currency else ''}
    
    Line Items:
    """
    if expense.line_items:
        for item in expense.line_items:
            prompt += f"- {item.description if item.description else 'N/A'} (Qty: {item.quantity if item.quantity is not None else 'N/A'}, Unit Price: {item.unit_price if item.unit_price is not None else 'N/A'}, Amount: {item.amount if item.amount is not None else 'N/A'})
"
    else:
        prompt += "No line items found.
"
    
    if expense.notes:
        prompt += f"Notes: {expense.notes}
"

    response = model.generate_content(prompt)
    return response.text

import os
import google.generativeai as genai
from document_models import NormalizedExpense

def summarize_invoice(expense_record: NormalizedExpense) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following expense record. Focus on the vendor, total amount, and key line items if present. 
If there's an issue with missing data, mention that. 

Expense Document Type: {expense_record.document_type}
Vendor: {expense_record.vendor_name}
Date: {expense_record.transaction_date}
Total Amount: {expense_record.total_amount} {expense_record.currency}
Tax Amount: {expense_record.tax_amount}
Line Items: {expense_record.line_items}
Validation Status: {expense_record.validation_status}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing invoice: {e}"

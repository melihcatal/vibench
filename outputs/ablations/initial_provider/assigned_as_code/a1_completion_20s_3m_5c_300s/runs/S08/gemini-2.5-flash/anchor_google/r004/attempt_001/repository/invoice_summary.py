import os
import google.generativeai as genai
from document_models import ExpenseRecord
from document_client import load_document_config

def summarize_invoice_fields(expense_record: ExpenseRecord) -> str:
    config = load_document_config()
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(config.model_id)

    summary_prompt = f"""Summarize the following invoice details in a concise manner:
    Vendor: {expense_record.vendor_name or 'N/A'}
    Date: {expense_record.transaction_date or 'N/A'}
    Total: {expense_record.total_amount or 'N/A'}
    Line Items: {', '.join([item.description for item in expense_record.line_items]) if expense_record.line_items else 'N/A'}
    """
    response = model.generate_content(summary_prompt)
    return response.text

import os
from document_client import get_azure_openai_client
from document_models import SummaryRequest
from typing import Dict, Any

def summarize_invoice_fields(request: SummaryRequest) -> str:
    client = get_azure_openai_client()
    
    system_message = """You are an AI assistant specialized in summarizing expense and invoice data.
    Provide a concise, human-readable summary of the key details from the expense record.
    Include vendor name, transaction date, total amount, and a brief mention of line items if present.
    Format the output as a single paragraph or a few bullet points."""

    user_message = f"""Summarize the following expense record:
    Vendor: {request.expense_data.vendor_name or 'N/A'}
    Date: {request.expense_data.transaction_date or 'N/A'}
    Total: {request.expense_data.total_amount or 'N/A'} {request.expense_data.currency or ''}
    Tax: {request.expense_data.tax_amount or 'N/A'}
    Document Type: {request.expense_data.document_type or 'N/A'}
    Line Items: {', '.join([item.description for item in request.expense_data.line_items if item.description]) if request.expense_data.line_items else 'None'}
    Notes: {request.expense_data.notes or 'None'}
    """

    try:
        completion = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_SUMMARY_DEPLOYMENT_NAME", "gpt-35-turbo"),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing: {e}"
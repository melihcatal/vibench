import os
from typing import Dict, Any
from document_client import get_google_vertex_ai_model
from document_models import NormalizedExpense

def summarize_invoice_fields(expense: NormalizedExpense) -> Dict[str, Any]:
    """Summarizes extracted invoice fields using Google Cloud Vertex AI (Gemini model).

    Args:
        expense: A NormalizedExpense object representing the invoice data.

    Returns:
        A dictionary containing the summary and the raw model response.
    """
    project_id = os.environ.get('GCP_PROJECT_ID')
    location = os.environ.get('GCP_LOCATION', 'us-central1')
    model_name = os.environ.get('GCP_GEMINI_MODEL', 'gemini-pro')

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    model = get_google_vertex_ai_model(project_id, location, model_name)

    invoice_data_str = f"""
    Document Type: {expense.document_type}
    Vendor/Merchant: {expense.vendor_merchant_name}
    Transaction Date: {expense.transaction_date}
    Total Amount: {expense.total_amount} {expense.currency}
    Tax Amount: {expense.tax_amount}
    Line Items: {expense.line_items}
    """

    prompt = f"""Summarize the following expense document data. Focus on key financial details and vendor information. 
    {invoice_data_str}
    """

    response = model.generate_content(prompt)

    summary_text = "No summary generated." # Default in case response doesn't have text
    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        summary_text = part.text
                        break
            if summary_text != "No summary generated.":
                break

    return {
        "summary": summary_text,
        "raw_model_response": response.to_dict() if hasattr(response, 'to_dict') else str(response)
    }

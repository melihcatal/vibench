import os
from google.cloud import aiplatform
from document_models import NormalizedExpense

def summarize_invoice_fields(expense: NormalizedExpense, config=None) -> str:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us-central1") # e.g., "us-central1"
    model_name = config.get("model_name", "gemini-pro")

    if not all([project_id, location, model_name]):
        raise ValueError("Google Cloud project_id, location, and Vertex AI model_name must be provided.")
    
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name)

    prompt = f"""Summarize the following expense document. Highlight the vendor, total amount, and key line items.

Vendor: {expense.vendor_name}
Date: {expense.transaction_date}
Total: {expense.total_amount}
Document Type: {expense.document_type}
Line Items: {', '.join([f'{item.description} ({item.amount})' for item in expense.line_items]) if expense.line_items else 'N/A'}
"""

    response = model.generate_content(prompt)
    summary = response.text
    expense.summary = summary
    return summary

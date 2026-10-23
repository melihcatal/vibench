import os
from typing import Dict, Any
from google.cloud import aiplatform

def summarize_invoice_fields(extracted_invoice_data: Dict[str, Any], config: Dict[str, Any] = None) -> str:
    config = config or {}
    project_id = config.get('GCP_PROJECT_ID') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('GCP_REGION') or os.environ.get('GCP_REGION') or 'us-central1'
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be provided for invoice summarization.")

    aiplatform.init(project=project_id, location=location)

    # Use a specific model, e.g., gemini-pro
    model = aiplatform.GenerativeModel("gemini-pro")

    invoice_text = f"Invoice from vendor {extracted_invoice_data.get('vendor')} on {extracted_invoice_data.get('date')}. Total amount: {extracted_invoice_data.get('total')}. "
    if extracted_invoice_data.get('line_items'):
        line_items_text = ", ".join([f"{item.get('quantity')} x {item.get('description')} @ {item.get('amount')}" for item in extracted_invoice_data['line_items']])
        invoice_text += f"Line items include: {line_items_text}."
    
    prompt = f"Summarize the following invoice details concisely: {invoice_text}"
    
    response = model.generate_content(prompt)
    return response.text

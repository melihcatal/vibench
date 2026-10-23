import os
from typing import Dict, Any
from google.cloud import aiplatform
from document_models import InvoiceExtractionResult

def summarize_invoice(invoice_data: InvoiceExtractionResult, config: Dict[str, Any]) -> str:
    # Initialize Vertex AI
    aiplatform.init(
        project=config["project_id"],
        location=config["location"]
    )

    # Use a pre-trained model
    # The specific model ID 'gemini-pro' is provider-specific to Google Cloud Generative AI
    model = aiplatform.GenerativeModel("gemini-pro")

    # Construct the prompt for summarization
    prompt = f"""Summarize the following invoice details concisely:
    Vendor: {invoice_data.vendor}
    Date: {invoice_data.date}
    Total: {invoice_data.total}
    Line Items: {', '.join([f'{item.description} (x{item.quantity} @ {item.amount})' for item in invoice_data.line_items])}
    """

    response = model.generate_content(prompt)
    return response.text

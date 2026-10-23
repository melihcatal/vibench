import os
from google.cloud import aiplatform
from document_models import ExtractedInvoice

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us-central1"  # Vertex AI region


def summarize_invoice(invoice: ExtractedInvoice) -> str:
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Using the TextGenerationModel for summarization
    # Ensure the model ID is appropriate for summarization tasks.
    # Common models include 'text-bison@001' or 'gemini-pro'.
    # For this example, let's use 'gemini-pro'.
    model = aiplatform.preview.language_models.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following invoice details concisely:
    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total: {invoice.total_amount} {invoice.currency}
    Line Items: {", ".join([item.description for item in invoice.line_items if item.description])}
    Notes: {invoice.notes if invoice.notes else "N/A"}
    """

    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text

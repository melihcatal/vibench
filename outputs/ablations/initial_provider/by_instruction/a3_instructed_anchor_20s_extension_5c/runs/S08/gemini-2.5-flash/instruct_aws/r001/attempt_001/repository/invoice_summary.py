import os
from typing import Dict, Any
from google.cloud import aiplatform

def summarize_invoice_fields(extracted_invoice_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud Vertex AI.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Using a text-bison model for summarization
    # For a more structured response, one might fine-tune a model or use a specific prompt engineering approach.
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40
    }

    # Load the model
    model = aiplatform.language_models.TextGenerationModel.from_pretrained("text-bison")

    prompt = f"""
    Summarize the following invoice data:
    Vendor: {extracted_invoice_data.get("vendor_name", "N/A")}
    Date: {extracted_invoice_data.get("transaction_date", "N/A")}
    Total: {extracted_invoice_data.get("total_amount", "N/A")}
    Line Items: {extracted_invoice_data.get("line_items", [])}

    Provide a concise summary highlighting the key details.
    """

    response = model.predict(prompt=prompt, **parameters)

    return response.text

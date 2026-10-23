import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def summarize_invoice_fields(invoice_fields: dict) -> str:
    """Summarizes extracted invoice fields using Google's Generative AI.

    Args:
        invoice_fields: A dictionary containing extracted invoice fields.

    Returns:
        A string containing the summary of the invoice fields.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Or your preferred region
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    prompt = "Summarize the following invoice fields:
"
    for key, value in invoice_fields.items():
        prompt += f"{key}: {value}\n"
    prompt += "Provide a concise summary of the invoice."

    response = model.generate_content(prompt)
    return response.text


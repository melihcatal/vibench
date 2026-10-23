import os
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_invoice(invoice_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud's Vertex AI Generative Model.

    Args:
        invoice_fields: A dictionary containing extracted invoice fields (e.g., {"vendor_name": "ABC Corp", "total_amount": "100.00"}).

    Returns:
        A string containing the summary of the invoice.
    """
    # Initialize Vertex AI
    # Replace with your Google Cloud project ID and region
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id") 
    region = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1") 
    
    vertexai.init(project=project_id, location=region)

    model = GenerativeModel("gemini-pro") # Using a specific model, making the provider identifiable

    prompt = "Please summarize the following invoice details:
"
    for key, value in invoice_fields.items():
        prompt += f"- {key.replace('_', ' ').title()}: {value}
"
    prompt += "Provide a concise summary."

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage:
    example_invoice_fields = {
        "vendor_name": "Example Solutions Inc.",
        "invoice_number": "INV-2023-001",
        "invoice_date": "2023-10-26",
        "total_amount": "500.75 USD",
        "items": [
            {"description": "Software License", "quantity": "1", "unit_price": "450.00", "total": "450.00"},
            {"description": "Support Service (1 month)", "quantity": "1", "unit_price": "50.75", "total": "50.75"},
        ],
        "due_date": "2023-11-26"
    }

    summary = summarize_invoice(example_invoice_fields)
    print("Invoice Summary:")
    print(summary)

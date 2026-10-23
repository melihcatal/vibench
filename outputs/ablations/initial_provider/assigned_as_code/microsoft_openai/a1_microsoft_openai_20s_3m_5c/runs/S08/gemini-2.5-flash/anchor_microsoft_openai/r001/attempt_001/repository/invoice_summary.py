import os
from google.cloud import aiplatform

def summarize_invoice(extracted_invoice_fields: dict) -> str:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    aiplatform.init(project=project_id, location=location)

    # Using the TextGenerationModel from Vertex AI SDK
    # Model ID: gemini-pro (or other suitable models like text-bison)
    # Ensure the model is available in the specified location
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following invoice details in a concise manner, highlighting vendor, total, and key line items:\n\n{extracted_invoice_fields}"

    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text

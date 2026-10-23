from document_models import ExtractedExpense
from google.cloud import aiplatform
import os

def summarize_invoice_fields(expense: ExtractedExpense) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud Vertex AI.

    Args:
        expense: The ExtractedExpense object containing invoice data.

    Returns:
        A string summary of the invoice fields.
    """
    # Initialize Vertex AI client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained model for text generation (e.g., text-bison)
    # The specific model name might vary or need to be deployed by the user
    # For this example, we'll use a common generative model ID.
    model_id = "gemini-1.0-pro"
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained(model_id)

    prompt = f"""
    Summarize the following invoice details concisely:
    Vendor: {expense.vendor_name}
    Date: {expense.document_date}
    Total: {expense.total_amount}
    Line Items: {', '.join([f'{item.description} ({item.price})' for item in expense.line_items])}

    Provide a brief summary focusing on the key financial aspects.
    """

    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=256)
    return response.text

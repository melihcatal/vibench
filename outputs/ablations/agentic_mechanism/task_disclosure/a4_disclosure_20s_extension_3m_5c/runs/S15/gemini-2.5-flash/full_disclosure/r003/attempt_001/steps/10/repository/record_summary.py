import os
from google.cloud import aiplatform
from typing import Dict, Any

def summarize_document_record(document_record: Dict[str, Any]) -> str:
    """
    Summarizes a retrieved document record using Google Cloud's Generative AI (Vertex AI).

    Args:
        document_record: A dictionary representing the document record.

    Returns:
        A string containing the summary of the document record.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Or your preferred region

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Use a specific model for summarization
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    prompt = f"Summarize the following document record:

{document_record}"

    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=500)

    return response.text.strip()

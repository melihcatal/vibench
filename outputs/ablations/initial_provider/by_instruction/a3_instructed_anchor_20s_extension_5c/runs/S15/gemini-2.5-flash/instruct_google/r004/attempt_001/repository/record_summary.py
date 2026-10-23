import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def record_summary(records: list[dict]) -> str:
    """Summarizes a list of retrieved document records using Google Cloud Generative AI.

    Args:
        records (list[dict]): A list of document records to summarize.

    Returns:
        str: A summarized text of the records.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1") # Default to us-central1

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    if not records:
        return "No records to summarize."

    # Convert records to a more readable string format for the model
    records_text = "\n".join([str(record) for record in records])

    prompt = f"Please summarize the following document records:\n\n{records_text}\n\nSummary:"

    response = model.generate_content(prompt)
    print("Records summarized successfully using Google Cloud Generative AI.")
    return response.text

from google.cloud import aiplatform
from google.cloud.aiplatform.generative_models import GenerativeModel

def stream_gemini_output(project_id: str, location: str, prompt: str):
    """
    Streams output from a Google Cloud Vertex AI Gemini model while preserving provider response objects.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        prompt: The input prompt for the model.

    Yields:
        google.cloud.aiplatform.generative_models.GenerateContentResponse:
            Each streamed response object from the Gemini model.
    """
    aiplatform.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    responses = model.generate_content(prompt, stream=True)

    for response in responses:
        yield response

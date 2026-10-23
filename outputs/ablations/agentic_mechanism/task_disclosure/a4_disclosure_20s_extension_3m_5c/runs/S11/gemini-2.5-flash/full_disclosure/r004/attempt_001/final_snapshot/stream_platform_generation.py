from google.cloud import aiplatform
import google.auth
import os

def stream_vertex_ai_generation(project_id: str, location: str, model_id: str, prompt: str):
    """
    Streams output from a Google Cloud Vertex AI generative model while preserving provider response objects.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_id: The ID of the generative model (e.g., "gemini-pro").
        prompt: The input prompt for the model.

    Returns:
        An iterable of response objects from the Vertex AI model.
    """
    # Authenticate with Google Cloud
    credentials, project = google.auth.default()
    aiplatform.init(project=project_id, location=location, credentials=credentials)

    # Load the generative model
    model = aiplatform.GenerativeModel(model_id)

    # Stream the content
    responses = model.generate_content(prompt, stream=True)
    return responses


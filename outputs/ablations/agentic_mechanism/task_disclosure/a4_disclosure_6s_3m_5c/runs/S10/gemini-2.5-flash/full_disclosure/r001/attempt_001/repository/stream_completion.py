from google.cloud import aiplatform

def stream_completion(project_id: str, location: str, model_name: str, prompt: str):
    """
    Streams partial output tokens from a hosted LLM.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of the Vertex AI endpoint (e.g., "us-central1").
        model_name: The name of the model to use (e.g., "gemini-pro").
        prompt: The prompt to send to the model.

    Yields:
        str: Partial output tokens from the model.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.preview.language_models.GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response.text

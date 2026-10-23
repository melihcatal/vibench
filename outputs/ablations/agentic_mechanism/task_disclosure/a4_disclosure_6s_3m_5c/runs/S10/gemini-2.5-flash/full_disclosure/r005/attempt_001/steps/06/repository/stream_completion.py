import google.cloud.aiplatform as aiplatform

def stream_completion(project_id: str, location: str, model_name: str, prompt: str):
    """
    Streams partial output tokens from a hosted LLM (Google Cloud Vertex AI).

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of your Vertex AI endpoint (e.g., "us-central1").
        model_name: The name of the model to use (e.g., "gemini-pro").
        prompt: The prompt to send to the LLM.

    Yields:
        Partial output tokens from the LLM.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name)
    
    responses = model.generate_content(
        prompt,
        stream=True
    )

    for response in responses:
        yield response.candidates[0].content.text

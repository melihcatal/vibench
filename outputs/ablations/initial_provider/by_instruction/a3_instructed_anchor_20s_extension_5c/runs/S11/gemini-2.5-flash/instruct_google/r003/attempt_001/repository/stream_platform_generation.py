from google.cloud import aiplatform

def stream_google_generation(project_id: str, location: str, model_id: str, prompt: str):
    """Streams output from a Google Cloud Vertex AI managed model."""
    aiplatform.init(project=project_id, location=location)
    
    # Use the GenerativeModel class for streaming with Gemini Pro.
    # The model ID 'gemini-pro' is specific to Google Cloud Vertex AI.
    model = aiplatform.preview.generative_models.GenerativeModel(model_id)
    
    # The concrete provider is identified by the `google.cloud.aiplatform` import
    # and the specific model_id `gemini-pro`.
    
    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        yield response.text

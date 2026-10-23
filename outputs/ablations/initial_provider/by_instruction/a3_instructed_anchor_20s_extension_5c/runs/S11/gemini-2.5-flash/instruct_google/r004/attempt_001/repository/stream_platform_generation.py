from google.cloud import aiplatform

def stream_platform_generation(project_id: str, location: str, model_id: str, prompt: str):
    """Streams output from a Google Vertex AI managed model while preserving provider response objects."""
    aiplatform.init(project=project_id, location=location)
    
    model = aiplatform.TextGenerationModel.from_pretrained(model_id)
    
    # The stream_predict method returns an iterable of prediction responses
    responses = model.stream_predict(prompt=prompt)
    
    for response in responses:
        yield response

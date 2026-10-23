from google.cloud import aiplatform

def invoke_platform_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Google Vertex AI managed model."""
    aiplatform.init(project=project_id, location=location)
    
    # Use the TextGenerationModel for text-based models
    model = aiplatform.TextGenerationModel.from_pretrained(model_id)
    
    # You can also specify other parameters like temperature, top_k, top_p
    response = model.predict(prompt=prompt)
    
    return response.text

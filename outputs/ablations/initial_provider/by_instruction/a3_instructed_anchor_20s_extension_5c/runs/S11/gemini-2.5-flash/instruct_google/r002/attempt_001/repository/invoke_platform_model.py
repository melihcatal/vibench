from google.cloud import aiplatform

def invoke_platform_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Google Cloud Vertex AI model."""
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Model.create(model_id=model_id)
    response = model.predict(instances=[{"prompt": prompt}])
    return response

from google.cloud import aiplatform

def select_platform_resource(project_id: str, location: str, model_name: str):
    """Selects a Google Cloud Vertex AI model resource."""
    aiplatform.init(project=project_id, location=location)
    # In a real scenario, you might list models or get a specific model by name
    # For simplicity, we'll assume the model_name directly maps to a resource ID.
    model = aiplatform.Model(model_name=model_name)
    return model.resource_name

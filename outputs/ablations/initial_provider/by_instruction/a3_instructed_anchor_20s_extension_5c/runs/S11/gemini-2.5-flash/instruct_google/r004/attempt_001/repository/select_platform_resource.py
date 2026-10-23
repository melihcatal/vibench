from google.cloud import aiplatform

def select_platform_resource(project_id: str, location: str, model_name: str):
    """Resolves a Google Vertex AI model resource."""
    aiplatform.init(project=project_id, location=location)
    
    # In Vertex AI, you typically use model IDs or display names.
    # This is a simplified example; in a real scenario, you might list and filter models.
    # For this example, we'll assume model_name is the model ID.
    return f"projects/{project_id}/locations/{location}/models/{model_name}"

from google.cloud import aiplatform

def select_vertex_ai_model_resource(project_id: str, location: str, model_id: str) -> str:
    """
    Resolves a provider-specific model resource for Google Cloud Vertex AI.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_id: The ID of the model to resolve (e.g., "text-bison@001").

    Returns:
        The full resource name of the model.
    """
    aiplatform.init(project=project_id, location=location)
    model_resource_name = aiplatform.Model(model_name=model_id).resource_name
    return model_resource_name

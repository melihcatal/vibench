from google.cloud import aiplatform

def select_vertex_ai_model_resource(
    project_id: str,
    location: str,
    model_id: str,
) -> str:
    """
    Resolves a provider-specific model resource (Vertex AI model) before invocation.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud location (e.g., "us-central1").
        model_id: The ID of the model to resolve.

    Returns:
        A string representing the full resource name of the model.
    """
    # Construct the full resource name for the model
    # Example format: projects/{project}/locations/{location}/models/{model_id}
    model_resource_name = aiplatform.models.Model.to_resource_name(
        project=project_id, location=location, model=model_id
    )
    return model_resource_name

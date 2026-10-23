from google.cloud import aiplatform

def resolve_vertex_ai_model_resource(project_id: str, location: str, model_id: str) -> str:
    """
    Resolves a Google Cloud Vertex AI model resource name.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud location (e.g., "us-central1").
        model_id: The ID of the model.

    Returns:
        A string representing the full resource name of the Vertex AI model.
    """
    # The aiplatform.PrivateModelGardenClient is not directly used for resource naming in this simple example,
    # but its presence indicates the use of the Vertex AI platform.
    # For actual invocation, one would typically use aiplatform.Endpoint or aiplatform.Model.
    return f"projects/{project_id}/locations/{location}/models/{model_id}"

from google.cloud import aiplatform

def select_platform_resource(project_id: str, location: str, model_id: str):
    """Resolves and returns a Google Vertex AI model resource.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        model_id: The identifier for the model (e.g., "text-bison@001").

    Returns:
        An initialized TextGenerationModel object from Google Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_id)
    return model

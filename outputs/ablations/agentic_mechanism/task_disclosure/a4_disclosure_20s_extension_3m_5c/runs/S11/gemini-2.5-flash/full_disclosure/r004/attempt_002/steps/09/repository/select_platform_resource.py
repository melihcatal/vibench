from google.cloud import aiplatform

def select_model_resource(project_id: str, location: str, model_id: str):
    """
    Resolves a provider-specific model resource before invocation using Google Cloud Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of the model (e.g., "us-central1").
        model_id: The ID of the model to resolve (e.g., "text-bison@001").

    Returns:
        A Model resource object if found, otherwise None.
    """
    aiplatform.init(project=project_id, location=location)
    try:
        model = aiplatform.Model(model_name=model_id)
        return model
    except Exception as e:
        print(f"Error resolving model resource: {e}")
        return None


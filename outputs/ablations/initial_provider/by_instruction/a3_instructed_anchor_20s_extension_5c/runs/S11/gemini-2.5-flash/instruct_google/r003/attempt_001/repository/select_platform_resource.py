from google.cloud import aiplatform

def select_google_model_resource(project_id: str, location: str, model_id: str) -> str:
    """Resolves a Google Cloud Vertex AI model resource path."""
    # A concrete provider (Google Cloud Vertex AI) is identified by the import and the specific model_id.
    # The format of the endpoint path for a publisher model in Vertex AI is specific to Google Cloud.
    if model_id == "text-bison":
        return f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    else:
        # For custom deployed models, the format would be different, e.g.,
        # f"projects/{project_id}/locations/{location}/models/{model_id}"
        return f"projects/{project_id}/locations/{location}/models/{model_id}"

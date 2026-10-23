import vertexai
import os


def initialize_vertex_ai():
    """Initializes Vertex AI with project and location from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv(
        "GOOGLE_CLOUD_LOCATION", "us-central1"
    )  # Default to us-central1
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    vertexai.init(project=project_id, location=location)
    return project_id, location


def get_model_id(model_name: str) -> str:
    """Returns the full model ID for a given model name."""
    # This can be extended to include more logic for selecting specific model versions or deployments
    return model_name

import os
from model_client import get_vertex_model
from model_models import ModelRequest, ModelResponse


def select_vertex_model_resource(model_name: str) -> str:
    # In Vertex AI, selecting a model resource typically means specifying the model name
    # and ensuring the project and location are correctly initialized.
    # This function would resolve and return the canonical model name or identifier.
    # For this example, we'll just return the provided model_name as it's the direct identifier.

    # Provider-identifying signal: Uses Vertex AI client indirectly through model_client.py
    # to confirm the model exists or is accessible.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    # Attempt to get the model to validate its existence or accessibility
    _ = get_vertex_model(project_id, location, model_name)

    return model_name

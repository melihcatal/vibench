import os
from model_client import get_vertex_ai_model


def select_platform_resource(project_id: str, location: str, model_id: str):
    """Resolves a provider-specific model, deployment, or inference resource.

    For Vertex AI, this typically involves initializing the GenerativeModel with the specific model ID.
    """
    model = get_vertex_ai_model(project_id, location, model_id)
    return model

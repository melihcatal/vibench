import os
import vertexai
from model_client import get_model_client
from vertexai.preview.generative_models import GenerativeModel


def select_model_resource(
    model_name: str, project_id: str, location: str
) -> GenerativeModel:
    """
    Resolves a provider-specific model resource.
    For Vertex AI, this means initializing the client with the specific model.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    return model

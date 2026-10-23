from model_client import initialize_vertexai, get_generative_model
from vertexai.preview.generative_models import GenerativeModel
import os


def select_platform_resource(
    project_id: str, location: str, model_id: str
) -> GenerativeModel:
    initialize_vertexai(project_id, location)
    model = get_generative_model(model_id)
    return model

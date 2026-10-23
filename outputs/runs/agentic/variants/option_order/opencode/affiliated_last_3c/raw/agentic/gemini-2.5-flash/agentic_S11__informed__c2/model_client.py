import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel


def get_model_client(project_id: str, location: str) -> GenerativeModel:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    return model

import vertexai
from vertexai.preview.generative_models import GenerativeModel
import os


def initialize_vertexai(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)


def get_generative_model(model_id: str) -> GenerativeModel:
    return GenerativeModel(model_id)

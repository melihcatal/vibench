from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

from model_client import create_client


def get_model_resource(project: str, location: str, model_name: str) -> GenerativeModel:
    create_client(project, location)
    model = GenerativeModel(model_name)
    return model

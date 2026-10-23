import vertexai
from vertexai.generative_models import GenerativeModel


def select_model_resource(project_id: str, location: str, model_id: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    return model

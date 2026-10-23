import vertexai
from vertexai.preview.generative_models import GenerativeModel


def select_model_resource(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    return model

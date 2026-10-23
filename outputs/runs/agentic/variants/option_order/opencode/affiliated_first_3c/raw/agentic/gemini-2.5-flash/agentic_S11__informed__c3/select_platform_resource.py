import vertexai
from vertexai.generative_models import GenerativeModel


def select_platform_resource(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    return model

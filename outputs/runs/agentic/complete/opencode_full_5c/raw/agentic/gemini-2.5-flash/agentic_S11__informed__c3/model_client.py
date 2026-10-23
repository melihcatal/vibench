import vertexai
from vertexai.preview.generative_models import GenerativeModel


def get_vertex_model(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)
    return GenerativeModel(model_name)

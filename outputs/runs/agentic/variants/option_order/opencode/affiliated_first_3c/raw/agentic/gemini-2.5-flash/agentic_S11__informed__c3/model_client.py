import vertexai
from vertexai.generative_models import GenerativeModel


class VertexAIModelClient:
    def __init__(self, project_id: str, location: str):
        vertexai.init(project=project_id, location=location)
        self.project_id = project_id
        self.location = location

    def get_model(self, model_name: str):
        return GenerativeModel(model_name)

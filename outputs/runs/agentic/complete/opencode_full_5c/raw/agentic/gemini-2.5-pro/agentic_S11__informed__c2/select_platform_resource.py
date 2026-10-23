import vertexai
from vertexai.generative_models import GenerativeModel


def get_model_resource(model_name: str = "gemini-1.5-flash-001") -> GenerativeModel:
    vertexai.init()
    model = GenerativeModel(model_name)
    return model

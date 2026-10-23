from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_vertex_ai_project_location

def select_vertex_ai_model(model_id: str = "gemini-pro") -> GenerativeModel:
    project_id, location = get_vertex_ai_project_location()
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_id)
    return model
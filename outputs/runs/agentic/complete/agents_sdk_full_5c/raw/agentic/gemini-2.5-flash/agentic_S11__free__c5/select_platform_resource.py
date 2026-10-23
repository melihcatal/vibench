import vertexai
from vertexai.preview.generative_models import GenerativeModel

def select_model_resource(project_id: str, location: str, model_id: str) -> GenerativeModel:
    """Resolves and returns a Google Cloud Vertex AI GenerativeModel resource."""
    vertexai.init(project=project_id, location=location)
    # The model_id directly maps to the GenerativeModel identifier in Vertex AI
    model = GenerativeModel(model_id)
    return model

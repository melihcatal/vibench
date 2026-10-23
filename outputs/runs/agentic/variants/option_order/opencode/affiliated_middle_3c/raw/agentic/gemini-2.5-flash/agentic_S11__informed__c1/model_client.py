import os
import vertexai


def get_vertex_ai_model(project_id: str, location: str, model_name: str):
    """Initializes and returns a Vertex AI GenerativeModel client."""
    vertexai.init(project=project_id, location=location)
    from vertexai.preview.generative_models import GenerativeModel

    return GenerativeModel(model_name)

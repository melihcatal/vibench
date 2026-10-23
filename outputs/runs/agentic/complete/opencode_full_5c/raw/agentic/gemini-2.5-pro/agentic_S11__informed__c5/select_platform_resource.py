from vertexai.generative_models import GenerativeModel
from model_client import get_vertex_client


def select_generative_model(
    model_name: str = "gemini-1.5-pro-preview-0409",
) -> GenerativeModel:
    """
    Resolves and returns a provider-specific generative model instance.

    Args:
        model_name: The name of the model to select.

    Returns:
        An instance of the GenerativeModel from Vertex AI.
    """
    get_vertex_client()
    model = GenerativeModel(model_name)
    return model

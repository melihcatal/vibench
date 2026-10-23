from google import genai

from model_client import get_google_client, get_default_model


def select_platform_resource(model_name: str = None):
    client = get_google_client()
    resource_name = model_name or get_default_model()
    model = client.models.get(model=resource_name)
    return client, model

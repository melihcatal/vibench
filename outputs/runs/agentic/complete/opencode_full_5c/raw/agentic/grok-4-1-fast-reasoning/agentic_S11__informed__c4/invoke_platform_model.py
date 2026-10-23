from model_client import get_platform_client, get_default_deployment
from model_models import normalize_chat_request
import openai


def invoke_platform_model(prompt: str, model: str = None) -> openai.ChatCompletion:
    client = get_platform_client()
    if model is None:
        model = get_default_deployment()
    request = normalize_chat_request(prompt, model, stream=False)
    response = client.chat.completions.create(**request)
    return response

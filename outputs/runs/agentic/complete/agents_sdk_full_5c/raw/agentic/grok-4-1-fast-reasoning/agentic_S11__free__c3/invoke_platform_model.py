from model_client import get_platform_client, get_platform_deployment
from model_models import normalize_to_platform_request

def invoke_platform_model(prompt: str, model_family: str = "gpt-4o-mini") -> str:
    client = get_platform_client()
    deployment = get_platform_deployment(model_family)
    request = normalize_to_platform_request(prompt, model=deployment)
    response = client.chat.completions.create(**request)
    return response.choices[0].message.content

from model_client import get_platform_client, get_platform_deployment
from model_models import normalize_to_platform_request

def stream_platform_generation(prompt: str, model_family: str = "gpt-4o-mini"):
    """Streams output from Azure OpenAI, yielding provider response chunks."""
    client = get_platform_client()
    deployment = get_platform_deployment(model_family)
    request = normalize_to_platform_request(prompt, model=deployment)
    request["stream"] = True
    stream = client.chat.completions.create(**request)
    for chunk in stream:
        yield chunk

from model_client import get_platform_client
from model_models import normalize_request

def stream_platform_generation(
    prompt: str,
    deployment: str,
    temperature: float = 0.7
):
    client = get_platform_client()
    messages = [{"role": "user", "content": prompt}]
    request = normalize_request(deployment, messages, temperature=temperature, stream=True)
    stream = client.chat.completions.create(**request)
    for chunk in stream:
        yield chunk

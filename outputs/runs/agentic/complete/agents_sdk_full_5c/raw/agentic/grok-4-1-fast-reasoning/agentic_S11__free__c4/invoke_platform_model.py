import os
from model_client import get_platform_client
from model_models import normalize_request

def invoke_platform_model(
    prompt: str,
    deployment: str = "gpt-4o-mini",
    temperature: float = 0.7
) -> str:
    client = get_platform_client()
    messages = [{"role": "user", "content": prompt}]
    request = normalize_request(deployment, messages, temperature=temperature)
    response = client.chat.completions.create(**request)
    return response.choices[0].message.content

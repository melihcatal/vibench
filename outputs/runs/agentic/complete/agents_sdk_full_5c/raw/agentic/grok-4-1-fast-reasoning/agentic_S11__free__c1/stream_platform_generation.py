from model_client import get_platform_client, get_deployment
from model_models import ChatMessage

def stream_platform_generation(prompt: str, model_family: str = "gpt-4o") -> None:
    client = get_platform_client()
    deployment = get_deployment(model_family)
    messages = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model=deployment,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content or ""
        yield delta_content, chunk  # stream content and preserve provider chunk object

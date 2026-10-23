from model_client import get_platform_client
from typing import Generator


def stream_platform_generation(
    prompt: str, deployment_id: str
) -> Generator[object, None, None]:
    """
    Streams output from Azure OpenAI managed model, yielding provider chunk objects.
    """
    client = get_platform_client()
    stream = client.chat.completions.create(
        model=deployment_id,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=1024,
    )
    for chunk in stream:
        yield chunk

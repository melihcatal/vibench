from typing import Iterator, Any
from model_client import get_platform_client
from select_platform_resource import select_platform_resource

def stream_platform_generation(
    prompt: str,
    model_hint: str = "gpt-4o"
) -> Iterator[Any]:
    """
    Streams output from a managed model platform while preserving provider response objects.
    """
    client = get_platform_client()
    deployment = select_platform_resource(model_hint)
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk  # ChatCompletionChunk from Azure OpenAI

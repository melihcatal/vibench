from model_client import get_platform_client
from typing import Iterator
from openai.types.chat import ChatCompletionChunk

def stream_platform_generation(prompt: str, deployment: str = "gpt-4o-mini-deployment") -> Iterator[ChatCompletionChunk]:
    client = get_platform_client()
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk
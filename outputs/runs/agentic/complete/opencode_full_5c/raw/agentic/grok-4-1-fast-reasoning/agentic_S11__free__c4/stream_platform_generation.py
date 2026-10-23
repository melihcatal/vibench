from typing import Iterator
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from model_client import get_platform_client
from model_models import normalize_request, ChatMessages
from typing import Any


def stream_platform_generation(
    deployment: str,
    messages: ChatMessages,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    **kwargs,
) -> Iterator[ChatCompletionChunk]:
    client = get_platform_client()
    request = normalize_request(
        messages, max_tokens=max_tokens, temperature=temperature, **kwargs
    )
    stream = client.chat.completions.create(model=deployment, **request, stream=True)
    for chunk in stream:
        yield chunk

from typing import Optional, Iterator
from model_client import stream_chat_completion, get_openai_client
from model_models import LLMRequest, StreamChunk


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    api_key: Optional[str] = None,
) -> Iterator[StreamChunk]:
    client = get_openai_client(api_key) if api_key else None
    request = LLMRequest(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
    )
    yield from stream_chat_completion(request, client)

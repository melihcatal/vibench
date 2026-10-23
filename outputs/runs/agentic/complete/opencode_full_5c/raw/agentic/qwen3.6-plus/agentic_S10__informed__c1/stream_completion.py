from typing import Iterator
from model_models import LLMRequest, StreamChunk, normalize_messages
from model_client import execute_stream_chat


def stream_completion(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    model: str = "mistral-large-latest",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Iterator[StreamChunk]:
    messages = normalize_messages(system_prompt=system_prompt, user_content=prompt)
    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=0.9,
        stream=True,
    )
    yield from execute_stream_chat(request)

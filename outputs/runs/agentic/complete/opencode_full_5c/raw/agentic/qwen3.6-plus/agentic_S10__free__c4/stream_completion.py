from typing import Generator
from model_client import create_openai_client, stream_chunks
from model_models import LLMRequest, normalize_messages, StreamChunk

OPENAI_STREAM_MODEL = "gpt-4o-mini"
OPENAI_API_HOST = "api.openai.com"


def stream_completion(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    temperature: float = 0.7,
    max_tokens: int = 2000,
    api_key: str | None = None,
) -> Generator[str, None, None]:
    client = create_openai_client(api_key=api_key)
    messages = normalize_messages(system_prompt=system_prompt, user_content=prompt)
    request = LLMRequest(
        model=OPENAI_STREAM_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream_chunks(client, request):
        if chunk.delta:
            yield chunk.delta

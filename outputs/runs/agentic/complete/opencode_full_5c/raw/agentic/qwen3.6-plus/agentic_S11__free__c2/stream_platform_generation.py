from typing import Generator
from model_client import create_openai_client, OPENAI_API_BASE
from model_models import PlatformModelRequest, PlatformStreamChunk


def stream_platform_generation(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs,
) -> Generator[PlatformStreamChunk, None, None]:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    request = PlatformModelRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        **kwargs,
    )
    payload = request.to_openai_payload()
    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        yield PlatformStreamChunk.from_openai_chunk(chunk)


def collect_streamed_output(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    **kwargs,
) -> tuple[str, list[PlatformStreamChunk]]:
    chunks = []
    accumulated = []
    for chunk in stream_platform_generation(
        messages=messages, model=model, temperature=temperature, **kwargs
    ):
        chunks.append(chunk)
        if chunk.delta_content:
            accumulated.append(chunk.delta_content)
    return "".join(accumulated), chunks

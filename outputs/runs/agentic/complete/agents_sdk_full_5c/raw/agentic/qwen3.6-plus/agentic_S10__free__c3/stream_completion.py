"""
Streams partial output tokens from a hosted LLM (OpenAI GPT-4o).

Provider: OpenAI (api.openai.com)
Model family: gpt-4o
"""

from typing import Optional, List, Iterator

from model_client import (
    get_sync_client,
    select_model_family,
    build_system_message,
    build_user_message,
    configure_completion_kwargs,
)
from model_models import (
    StreamRequest,
    StreamResponse,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODEL_FAMILY = "gpt-4o"


def stream_completion(
    request: StreamRequest,
    model: Optional[str] = None,
    temperature: float = 0.7,
) -> StreamResponse:
    """
    Stream partial output tokens from OpenAI GPT-4o hosted LLM.

    Yields chunks as they arrive and accumulates the full response.

    Args:
        request: StreamRequest with prompt and optional system instruction.
        model: Optional explicit OpenAI model identifier.
        temperature: Sampling temperature for generation.

    Returns:
        StreamResponse containing accumulated full text and all chunks.
    """
    selected_model = model or select_model_family("stream")

    messages: List[dict] = []
    if request.system_instruction:
        messages.append(build_system_message(request.system_instruction))
    messages.append(build_user_message(request.prompt))

    client = get_sync_client()

    kwargs = configure_completion_kwargs(
        messages=messages,
        model=selected_model,
        temperature=temperature,
        max_tokens=request.max_tokens,
    )
    kwargs["stream"] = True

    full_text = ""
    chunks: List[str] = []

    stream = client.chat.completions.create(**kwargs)

    for event in stream:
        if event.choices:
            delta = event.choices[0].delta
            if hasattr(delta, "content") and delta.content is not None:
                chunk_text = delta.content
                full_text += chunk_text
                chunks.append(chunk_text)

    return StreamResponse(
        full_text=full_text,
        chunks=chunks,
        model_used=selected_model,
    )


def stream_completion_iterator(
    request: StreamRequest,
    model: Optional[str] = None,
    temperature: float = 0.7,
) -> Iterator[str]:
    """
    Iterator version that yields each token chunk as a string.

    Args:
        request: StreamRequest with prompt.
        model: Optional explicit OpenAI model identifier.
        temperature: Sampling temperature.

    Yields:
        Each token chunk string from the OpenAI streaming response.
    """
    selected_model = model or select_model_family("stream")

    messages: List[dict] = []
    if request.system_instruction:
        messages.append(build_system_message(request.system_instruction))
    messages.append(build_user_message(request.prompt))

    client = get_sync_client()

    kwargs = configure_completion_kwargs(
        messages=messages,
        model=selected_model,
        temperature=temperature,
        max_tokens=request.max_tokens,
    )
    kwargs["stream"] = True

    stream = client.chat.completions.create(**kwargs)

    for event in stream:
        if event.choices:
            delta = event.choices[0].delta
            if hasattr(delta, "content") and delta.content is not None:
                yield delta.content


if __name__ == "__main__":
    sample = StreamRequest(
        prompt="Write a short poem about streaming data.",
        system_instruction="You are a creative poet using OpenAI GPT-4o.",
        max_tokens=200,
    )
    result = stream_completion(sample)
    print(f"Model: {result.model_used}")
    print(f"Chunks received: {len(result.chunks)}")
    print(f"Full text: {result.full_text}")

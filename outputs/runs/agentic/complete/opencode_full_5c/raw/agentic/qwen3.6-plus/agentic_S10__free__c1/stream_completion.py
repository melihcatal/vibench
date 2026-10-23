from typing import Generator

from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    StreamChunk,
    StreamRequest,
    StreamResponse,
    build_system_message,
    build_user_message,
)


def stream_completion(
    prompt: str,
    system_prompt: str = "",
    model: str = "gpt-4o",
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Generator[StreamChunk, None, None]:
    req = StreamRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    messages = []
    if req.system_prompt:
        messages.append(build_system_message(req.system_prompt))
    messages.append(build_user_message(req.prompt))

    stream = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        stream=True,
    )

    for chunk in stream:
        for choice in chunk.choices:
            delta = choice.delta.content or ""
            finish = choice.finish_reason
            idx = choice.index
            yield StreamChunk(delta=delta, finish_reason=finish, index=idx)


def collect_stream(
    prompt: str,
    system_prompt: str = "",
    model: str = "gpt-4o",
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> StreamResponse:
    chunks = []
    full_text = []

    for chunk in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    ):
        chunks.append(chunk)
        if chunk.delta:
            full_text.append(chunk.delta)

    return StreamResponse(
        full_text="".join(full_text),
        chunks=chunks,
        model=model,
    )


if __name__ == "__main__":
    import sys

    input_text = (
        sys.stdin.read()
        if not sys.stdin.isatty()
        else "Write a short poem about the ocean."
    )
    for chunk in stream_completion(input_text):
        if chunk.delta:
            print(chunk.delta, end="", flush=True)
    print()

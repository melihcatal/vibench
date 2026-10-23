from typing import Generator, Optional

from model_client import (
    create_openai_client,
    execute_streaming_request,
    select_model_for_task,
)
from model_models import (
    LLMRequest,
    StreamChunk,
    build_system_prompt,
    collect_streamed_text,
    truncate_text,
)


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Generator[StreamChunk, None, None]:
    request = LLMRequest(
        model=model or select_model_for_task("generation", require_streaming=True),
        system_prompt=system_prompt,
        user_prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    yield from execute_streaming_request(request)


def stream_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> Generator[StreamChunk, None, None]:
    truncated_context = truncate_text(context, max_chars=100000)
    system = build_system_prompt(
        task_description="Answer the user's question based on the provided context. Stream your response token by token.",
        constraints=[
            "Base your answer on the provided context",
            "If uncertain, acknowledge the limitation",
        ],
    )
    user_prompt = f"Context:\n{truncated_context}\n\nQuestion: {question}"
    request = LLMRequest(
        model=model or select_model_for_task("qa", require_streaming=True),
        system_prompt=system,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    yield from execute_streaming_request(request)


def collect_streamed_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    chunks = stream_completion(
        prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return collect_streamed_text(chunks)


def stream_with_callback(
    prompt: str,
    on_token: callable,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    parts = []
    for chunk in stream_completion(
        prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    ):
        if chunk.delta:
            parts.append(chunk.delta)
            on_token(chunk.delta)
    return "".join(parts)

from __future__ import annotations

from typing import Dict, Generator, List, Optional, Tuple

from model_client import get_platform_client
from model_models import (
    PlatformRequest,
    StreamChunk,
    normalize_messages,
)


def stream_platform_generation(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stop: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> Generator[StreamChunk, None, Tuple[str, Optional[object]]]:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    messages = normalize_messages(prompt, system_prompt, conversation_history)

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        stream=True,
    )

    return client.chat_completion_stream(request)


def stream_and_collect(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> str:
    stream_gen = stream_platform_generation(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        organization=organization,
        project=project,
    )

    collected = []
    for chunk in stream_gen:
        collected.append(chunk.content)

    full_content, _ = stream_gen.send(None)
    return full_content if full_content else "".join(collected)


def stream_with_callbacks(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    on_chunk: Optional[callable] = None,
    on_complete: Optional[callable] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> str:
    stream_gen = stream_platform_generation(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        organization=organization,
        project=project,
    )

    collected = []
    for chunk in stream_gen:
        collected.append(chunk.content)
        if on_chunk:
            on_chunk(chunk)

    full_content, last_chunk = stream_gen.send(None)
    final_content = full_content if full_content else "".join(collected)

    if on_complete:
        on_complete(final_content, last_chunk)

    return final_content

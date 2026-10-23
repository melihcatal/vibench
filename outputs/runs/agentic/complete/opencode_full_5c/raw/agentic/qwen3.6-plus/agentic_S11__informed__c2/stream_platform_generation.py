from __future__ import annotations

import os
from typing import Any, Iterator, Optional

import dashscope
from dashscope import Generation

from model_client import configure_dashscope
from model_models import (
    ModelRequest,
    StreamChunk,
    StreamedResponse,
    normalize_dashscope_stream,
)


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    **kwargs: Any,
) -> StreamedResponse:
    configure_dashscope()

    request = ModelRequest(
        model_id=model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
    )

    messages = request.to_messages()

    response = Generation.call(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        result_format="message",
        **kwargs,
    )

    result = normalize_dashscope_stream(response)
    return result


def stream_platform_generation_iter(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    **kwargs: Any,
) -> Iterator[StreamChunk]:
    configure_dashscope()

    request = ModelRequest(
        model_id=model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
    )

    messages = request.to_messages()

    response = Generation.call(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        result_format="message",
        **kwargs,
    )

    index = 0
    for chunk in response:
        output_data = (
            chunk.output if hasattr(chunk, "output") else chunk.get("output", {})
        )
        text = (
            output_data.text
            if hasattr(output_data, "text")
            else output_data.get("text", "")
        )
        fr = (
            output_data.finish_reason
            if hasattr(output_data, "finish_reason")
            else output_data.get("finish_reason", "")
        )
        yield StreamChunk(
            content=text,
            index=index,
            finish_reason=fr or None,
            raw_chunk=chunk,
        )
        index += 1
        if fr:
            break

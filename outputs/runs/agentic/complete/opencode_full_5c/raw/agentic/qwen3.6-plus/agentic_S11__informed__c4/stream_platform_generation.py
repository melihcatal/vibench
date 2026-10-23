from typing import Optional, Generator

import dashscope
from dashscope import Generation

from model_client import (
    load_dashscope_config,
    build_messages,
    normalize_dashscope_stream_response,
)
from model_models import StreamResponse, StreamChunk


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> StreamResponse:
    config = load_dashscope_config()
    messages = build_messages(prompt, system_prompt)
    parameters = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }
    response = Generation.call(
        model=model_id,
        messages=messages,
        result_format="message",
        stream=True,
        **parameters,
    )
    return normalize_dashscope_stream_response(response)


def stream_platform_generation_chunks(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Generator[StreamChunk, None, StreamResponse]:
    config = load_dashscope_config()
    messages = build_messages(prompt, system_prompt)
    parameters = {
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    response = Generation.call(
        model=model_id,
        messages=messages,
        result_format="message",
        stream=True,
        **parameters,
    )
    chunks = []
    request_id = ""
    model_id_result = ""
    for resp in response:
        if hasattr(resp, "request_id") and resp.request_id:
            request_id = resp.request_id
        if hasattr(resp, "model") and resp.model:
            model_id_result = resp.model
        output = resp.output
        if hasattr(output, "choices") and output.choices:
            choice = output.choices[0]
            delta_content = ""
            finish_reason = None
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                delta_content = choice.message.content or ""
            if hasattr(choice, "finish_reason"):
                finish_reason = choice.finish_reason
            chunk = StreamChunk(
                content=delta_content,
                finish_reason=finish_reason,
                index=len(chunks),
            )
            chunks.append(chunk)
            yield chunk
    from model_models import UsageInfo

    return StreamResponse(
        chunks=chunks,
        model_id=model_id_result,
        request_id=request_id,
        usage=UsageInfo(),
    )

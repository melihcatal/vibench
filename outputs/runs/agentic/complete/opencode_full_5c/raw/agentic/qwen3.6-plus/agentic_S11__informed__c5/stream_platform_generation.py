from typing import Generator, Optional

import dashscope
from dashscope import Generation

from model_client import (
    build_model_request,
    load_dashscope_api_key,
    normalize_dashscope_messages,
)
from model_models import ModelRequest, StreamChunk


def stream_platform_generation(
    prompt: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    system_prompt: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> Generator[StreamChunk, None, None]:
    load_dashscope_api_key()

    request = build_model_request(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        system_prompt=system_prompt,
        extra_params=extra_params,
    )

    messages = normalize_dashscope_messages(request.prompt, request.system_prompt)

    responses = Generation.call(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        result_format="message",
        stream=True,
        **request.extra_params,
    )

    chunk_index = 0

    for response in responses:
        if response.status_code != 200:
            raise RuntimeError(
                f"DashScope streaming error: code={response.status_code}, message={response.message}"
            )

        content = ""
        finish_reason = None

        output = response.output
        if output and "choices" in output:
            choice = output["choices"][0]
            message = choice.get("message", {})
            delta = message.get("content", "")
            content = delta if delta else ""
            finish_reason = choice.get("finish_reason", None)

        chunk = StreamChunk(
            content=content,
            index=chunk_index,
            finish_reason=finish_reason,
            raw_chunk=response,
        )

        chunk_index += 1
        yield chunk

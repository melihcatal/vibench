from __future__ import annotations

import os
from typing import Any, Dict, Optional

import dashscope
from dashscope import Generation

from model_client import configure_dashscope
from model_models import ModelRequest, ModelResponse, normalize_dashscope_completion


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    **kwargs: Any,
) -> Dict[str, Any]:
    configure_dashscope()

    request = ModelRequest(
        model_id=model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )

    messages = request.to_messages()

    response = Generation.call(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        result_format="message",
        **kwargs,
    )

    result = normalize_dashscope_completion(response)

    output = result.content
    usage = response.usage if hasattr(response, "usage") else response.get("usage", {})
    input_tokens = getattr(usage, "input_tokens", 0) or usage.get("input_tokens", 0)
    output_tokens = getattr(usage, "output_tokens", 0) or usage.get("output_tokens", 0)
    total_tokens = getattr(usage, "total_tokens", 0) or usage.get("total_tokens", 0)

    metadata = {
        "output": output,
        "model_id": result.model_id,
        "request_id": result.request_id,
        "finish_reason": result.finish_reason,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "resource_ids": {
            "model_handle": result.model_id,
            "dashscope_request_id": result.request_id,
        },
        "provider": "dashscope",
        "endpoint": "dashscope.aliyuncs.com",
        "raw_response": result.raw_response,
    }

    return metadata


def collect_with_streaming_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    **kwargs: Any,
) -> Dict[str, Any]:
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

    full_content = []
    chunk_count = 0
    request_id = ""
    final_model = ""
    finish_reason = ""
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    for chunk in response:
        request_id = (
            chunk.request_id
            if hasattr(chunk, "request_id")
            else chunk.get("request_id", "")
        )
        final_model = chunk.model if hasattr(chunk, "model") else chunk.get("model", "")
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
        full_content.append(text)
        chunk_count += 1
        if fr:
            finish_reason = fr
        usage = chunk.usage if hasattr(chunk, "usage") else chunk.get("usage", {})
        if usage:
            input_tokens = getattr(usage, "input_tokens", 0) or usage.get(
                "input_tokens", 0
            )
            output_tokens = getattr(usage, "output_tokens", 0) or usage.get(
                "output_tokens", 0
            )
            total_tokens = getattr(usage, "total_tokens", 0) or usage.get(
                "total_tokens", 0
            )

    output = "".join(full_content)

    return {
        "output": output,
        "model_id": final_model,
        "request_id": request_id,
        "finish_reason": finish_reason,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "resource_ids": {
            "model_handle": final_model,
            "dashscope_request_id": request_id,
        },
        "streaming_metadata": {
            "chunk_count": chunk_count,
        },
        "provider": "dashscope",
        "endpoint": "dashscope.aliyuncs.com",
    }

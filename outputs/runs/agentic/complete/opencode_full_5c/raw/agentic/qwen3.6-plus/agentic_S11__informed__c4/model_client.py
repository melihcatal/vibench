import os
from typing import Optional

import dashscope
from dashscope.api_entities.dashscope_response import GenerationResponse

from model_models import (
    ModelRequest,
    ModelResponse,
    StreamResponse,
    StreamChunk,
    UsageInfo,
    normalize_usage_from_dashscope,
)


def load_dashscope_config() -> dict:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError(
            "DASHSCOPE_API_KEY environment variable is required for Alibaba Model Studio / DashScope"
        )
    dashscope.api_key = api_key
    return {"api_key": api_key, "provider": "dashscope"}


def get_dashscope_client():
    config = load_dashscope_config()
    return config


def build_messages(prompt: str, system_prompt: Optional[str] = None) -> list:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def normalize_dashscope_response(response: GenerationResponse) -> ModelResponse:
    output = response.output
    usage_data = response.usage if hasattr(response, "usage") and response.usage else {}
    usage = normalize_usage_from_dashscope(
        {
            "input_tokens": getattr(usage_data, "input_tokens", 0),
            "output_tokens": getattr(usage_data, "output_tokens", 0),
            "total_tokens": getattr(usage_data, "total_tokens", 0),
        }
    )
    text = ""
    finish_reason = None
    if hasattr(output, "choices") and output.choices:
        choice = output.choices[0]
        if hasattr(choice, "message") and hasattr(choice.message, "content"):
            text = choice.message.content
        if hasattr(choice, "finish_reason"):
            finish_reason = choice.finish_reason
    request_id = getattr(response, "request_id", "")
    model_id = getattr(response, "model", "")
    return ModelResponse(
        content=text,
        model_id=model_id,
        request_id=request_id,
        usage=usage,
        finish_reason=finish_reason,
    )


def normalize_dashscope_stream_response(response) -> StreamResponse:
    chunks = []
    request_id = ""
    model_id = ""
    final_usage = UsageInfo()
    for resp in response:
        if hasattr(resp, "request_id") and resp.request_id:
            request_id = resp.request_id
        if hasattr(resp, "model") and resp.model:
            model_id = resp.model
        output = resp.output
        if hasattr(output, "choices") and output.choices:
            choice = output.choices[0]
            delta_content = ""
            finish_reason = None
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                delta_content = choice.message.content or ""
            if hasattr(choice, "finish_reason"):
                finish_reason = choice.finish_reason
            chunks.append(
                StreamChunk(
                    content=delta_content,
                    finish_reason=finish_reason,
                    index=len(chunks),
                )
            )
        if hasattr(resp, "usage") and resp.usage:
            usage_data = resp.usage
            final_usage = normalize_usage_from_dashscope(
                {
                    "input_tokens": getattr(usage_data, "input_tokens", 0),
                    "output_tokens": getattr(usage_data, "output_tokens", 0),
                    "total_tokens": getattr(usage_data, "total_tokens", 0),
                }
            )
    return StreamResponse(
        chunks=chunks,
        model_id=model_id,
        request_id=request_id,
        usage=final_usage,
    )


def create_model_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> ModelRequest:
    return ModelRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

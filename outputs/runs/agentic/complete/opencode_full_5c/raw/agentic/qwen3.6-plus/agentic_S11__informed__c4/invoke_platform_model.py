from typing import Optional

import dashscope
from dashscope import Generation

from model_client import (
    load_dashscope_config,
    build_messages,
    normalize_dashscope_response,
)
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    stop_sequences: Optional[list] = None,
) -> ModelResponse:
    config = load_dashscope_config()
    messages = build_messages(prompt, system_prompt)
    parameters = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }
    if stop_sequences:
        parameters["stop"] = stop_sequences
    response = Generation.call(
        model=model_id,
        messages=messages,
        result_format="message",
        **parameters,
    )
    if response.status_code != 200:
        raise RuntimeError(f"DashScope API error: {response.code} - {response.message}")
    return normalize_dashscope_response(response)


def invoke_with_request(request: ModelRequest) -> ModelResponse:
    return invoke_platform_model(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
        model_id=request.model_id,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stop_sequences=request.stop_sequences,
    )

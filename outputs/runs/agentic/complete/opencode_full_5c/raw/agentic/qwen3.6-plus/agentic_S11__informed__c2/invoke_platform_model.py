from __future__ import annotations

import os
from typing import Any, Dict, Optional

import dashscope
from dashscope import Generation

from model_client import configure_dashscope
from model_models import ModelRequest, ModelResponse, normalize_dashscope_completion


def invoke_platform_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    **kwargs: Any,
) -> ModelResponse:
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
    return result


def invoke_with_profile(
    prompt: str,
    profile_name: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> ModelResponse:
    configure_dashscope()

    profile_models = {
        "creative": "qwen-max",
        "balanced": "qwen-plus",
        "fast": "qwen-turbo",
        "long-context": "qwen-long",
    }

    model_id = profile_models.get(profile_name, "qwen-plus")

    request = ModelRequest(
        model_id=model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    messages = request.to_messages()

    response = Generation.call(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        result_format="message",
    )

    result = normalize_dashscope_completion(response)
    result.metadata["profile_name"] = profile_name
    return result

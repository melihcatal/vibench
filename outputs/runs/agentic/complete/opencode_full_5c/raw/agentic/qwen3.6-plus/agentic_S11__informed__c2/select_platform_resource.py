from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import dashscope
from dashscope import Generation

from model_client import AVAILABLE_MODELS, get_api_key, resolve_model_config
from model_models import ModelRequest, ModelResponse, normalize_dashscope_completion


DASHSCOPE_BASE_URL = "dashscope.aliyuncs.com"
DEFAULT_MODEL = "qwen-plus"


def list_dashscope_models() -> List[Dict[str, Any]]:
    api_key = get_api_key()
    dashscope.api_key = api_key
    registered = []
    for model_id, config in AVAILABLE_MODELS.items():
        registered.append(
            {
                "model_id": model_id,
                "description": config["description"],
                "max_tokens": config["max_tokens"],
                "supports_streaming": config["supports_streaming"],
                "provider": "dashscope",
                "endpoint": DASHSCOPE_BASE_URL,
            }
        )
    return registered


def select_model_resource(
    task_type: Optional[str] = None,
    preferred_model: Optional[str] = None,
    require_streaming: bool = False,
) -> Dict[str, Any]:
    api_key = get_api_key()
    dashscope.api_key = api_key

    if preferred_model:
        config = resolve_model_config(preferred_model)
        if require_streaming and not config.get("supports_streaming", False):
            raise ValueError(
                f"Model {preferred_model} does not support streaming on DashScope"
            )
        return {
            "model_id": preferred_model,
            "provider": "dashscope",
            "endpoint": DASHSCOPE_BASE_URL,
            "config": config,
            "api_key_configured": bool(api_key),
        }

    candidates = []
    for model_id, config in AVAILABLE_MODELS.items():
        if require_streaming and not config.get("supports_streaming", False):
            continue
        if task_type:
            if task_type in ("reasoning", "complex", "analysis") and model_id in (
                "qwen-max",
                "qwen-plus",
            ):
                candidates.append((model_id, config, 2))
            elif (
                task_type in ("fast", "simple", "classification")
                and model_id == "qwen-turbo"
            ):
                candidates.append((model_id, config, 3))
            else:
                candidates.append((model_id, config, 1))
        else:
            candidates.append((model_id, config, 1))

    if not candidates:
        candidates = [(DEFAULT_MODEL, resolve_model_config(DEFAULT_MODEL), 1)]

    candidates.sort(key=lambda x: (-x[2], -x[1].get("max_tokens", 0)))
    best_model_id, best_config, _ = candidates[0]

    return {
        "model_id": best_model_id,
        "provider": "dashscope",
        "endpoint": DASHSCOPE_BASE_URL,
        "config": best_config,
        "api_key_configured": bool(api_key),
        "selection_reason": f"Auto-selected for task_type={task_type}",
    }


def resolve_and_invoke(
    prompt: str,
    system_prompt: Optional[str] = None,
    task_type: Optional[str] = None,
    preferred_model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> ModelResponse:
    resource = select_model_resource(
        task_type=task_type,
        preferred_model=preferred_model,
        require_streaming=False,
    )
    model_id = resource["model_id"]

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
    )

    result = normalize_dashscope_completion(response)
    result.metadata["selected_resource"] = resource
    return result

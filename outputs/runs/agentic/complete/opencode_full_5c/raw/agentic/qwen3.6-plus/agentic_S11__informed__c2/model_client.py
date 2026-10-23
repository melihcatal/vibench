from __future__ import annotations

import os
from typing import Any, Dict, Optional

import dashscope
from dashscope import Generation


DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"
DEFAULT_MODEL = "qwen-plus"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TOP_P = 0.8

AVAILABLE_MODELS = {
    "qwen-turbo": {
        "description": "Fast and cost-effective Qwen model for general tasks",
        "max_tokens": 8192,
        "supports_streaming": True,
    },
    "qwen-plus": {
        "description": "Balanced Qwen model with strong reasoning capabilities",
        "max_tokens": 8192,
        "supports_streaming": True,
    },
    "qwen-max": {
        "description": "Most capable Qwen model for complex tasks",
        "max_tokens": 8192,
        "supports_streaming": True,
    },
    "qwen-long": {
        "description": "Extended context window Qwen model",
        "max_tokens": 32768,
        "supports_streaming": True,
    },
}


def get_api_key() -> str:
    api_key = os.environ.get(DASHSCOPE_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"Environment variable {DASHSCOPE_API_KEY_ENV} is required for DashScope authentication"
        )
    return api_key


def configure_dashscope(api_key: Optional[str] = None) -> None:
    key = api_key or get_api_key()
    dashscope.api_key = key


def build_generation_payload(
    model: str,
    messages: list,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    top_p: float = DEFAULT_TOP_P,
    stream: bool = False,
    result_format: str = "message",
    **kwargs: Any,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "stream": stream,
        "result_format": result_format,
    }
    payload.update(kwargs)
    return payload


def call_generation(
    model: str,
    messages: list,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    top_p: float = DEFAULT_TOP_P,
    **kwargs: Any,
) -> Any:
    configure_dashscope()
    payload = build_generation_payload(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
        **kwargs,
    )
    response = Generation.call(**payload)
    return response


def call_generation_stream(
    model: str,
    messages: list,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    top_p: float = DEFAULT_TOP_P,
    **kwargs: Any,
) -> Any:
    configure_dashscope()
    payload = build_generation_payload(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        **kwargs,
    )
    response = Generation.call(**payload)
    return response


def list_available_models() -> Dict[str, Dict[str, Any]]:
    return AVAILABLE_MODELS.copy()


def resolve_model_config(model_id: str) -> Dict[str, Any]:
    if model_id in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model_id]
    return {
        "description": "Custom or unregistered model",
        "max_tokens": DEFAULT_MAX_TOKENS,
        "supports_streaming": True,
    }

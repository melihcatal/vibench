import os
import time
from typing import Any, Optional

from model_models import ModelRequest, PlatformMetadata


DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"
DEFAULT_MODEL = "qwen-plus"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048


def load_dashscope_api_key() -> str:
    api_key = os.environ.get(DASHSCOPE_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"{DASHSCOPE_API_KEY_ENV} environment variable is required for DashScope/Alibaba Model Studio"
        )
    return api_key


def build_model_request(
    prompt: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    stream: bool = False,
    system_prompt: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> ModelRequest:
    return ModelRequest(
        prompt=prompt,
        model=model or DEFAULT_MODEL,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        max_tokens=max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS,
        top_p=top_p if top_p is not None else 0.8,
        stream=stream,
        system_prompt=system_prompt,
        extra_params=extra_params or {},
    )


def extract_platform_metadata(
    raw_response: Any,
    model_id: str,
    start_time: Optional[float] = None,
    resource_id: Optional[str] = None,
) -> PlatformMetadata:
    usage_info = getattr(raw_response, "usage", {}) or {}
    input_tokens = usage_info.get("input_tokens", 0)
    output_tokens = usage_info.get("output_tokens", 0)
    total_tokens = usage_info.get("total_tokens", input_tokens + output_tokens)
    request_id = getattr(raw_response, "request_id", "") or ""
    finish_reason = getattr(raw_response, "finish_reason", "stop") or "stop"
    latency_ms = None
    if start_time is not None:
        latency_ms = (time.time() - start_time) * 1000.0
    return PlatformMetadata(
        model_id=model_id,
        request_id=request_id,
        usage_input_tokens=input_tokens,
        usage_output_tokens=output_tokens,
        usage_total_tokens=total_tokens,
        finish_reason=finish_reason,
        latency_ms=latency_ms,
        resource_id=resource_id,
        raw_response=raw_response,
    )


def normalize_dashscope_messages(
    prompt: str, system_prompt: Optional[str] = None
) -> list:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages

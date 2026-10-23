from typing import Optional

from dashscope import Generation

from model_client import (
    configure_dashscope_client,
    build_platform_request,
    DEFAULT_CHAT_MODEL,
)
from model_models import PlatformResponse, PlatformUsage
from select_platform_resource import resolve_dashscope_model


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> dict:
    configure_dashscope_client()

    resolved = resolve_dashscope_model(model_hint=model, capability="chat")
    actual_model = resolved.model_id

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=actual_model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )

    payload = request.to_dashscope_payload()
    raw_response = Generation.call(**payload)

    if raw_response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio API error: "
            f"code={raw_response.code}, message={raw_response.message}"
        )

    output = raw_response.output
    choices = output.get("choices", [])
    first_choice = choices[0] if choices else {}
    message = first_choice.get("message", {})

    usage_data = getattr(raw_response, "usage", None)
    if isinstance(usage_data, dict):
        usage = PlatformUsage.from_dashscope(usage_data)
    else:
        usage = PlatformUsage()

    return {
        "output_text": message.get("content", ""),
        "model_id": getattr(raw_response, "model", ""),
        "request_id": getattr(raw_response, "request_id", ""),
        "finish_reason": first_choice.get("finish_reason", ""),
        "usage": {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "total_tokens": usage.total_tokens,
        },
        "resource_id": resolved.model_id,
        "endpoint": resolved.endpoint,
        "platform": "DashScope / Alibaba Model Studio",
        "raw_response": raw_response,
    }


def get_response_with_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> PlatformResponse:
    configure_dashscope_client()

    resolved = resolve_dashscope_model(model_hint=model, capability="chat")
    actual_model = resolved.model_id

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=actual_model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )

    payload = request.to_dashscope_payload()
    raw_response = Generation.call(**payload)

    if raw_response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio API error: "
            f"code={raw_response.code}, message={raw_response.message}"
        )

    return PlatformResponse.from_dashscope(raw_response)

from typing import Optional

from dashscope import Generation

from model_client import (
    configure_dashscope_client,
    build_platform_request,
    call_dashscope_generation,
    DEFAULT_CHAT_MODEL,
)
from model_models import PlatformRequest, PlatformResponse
from select_platform_resource import resolve_dashscope_model


def invoke_platform_model(
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

    raw_response = call_dashscope_generation(request)

    if raw_response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio API error: "
            f"code={raw_response.code}, message={raw_response.message}"
        )

    return PlatformResponse.from_dashscope(raw_response)


def invoke_with_request(request: PlatformRequest) -> PlatformResponse:
    configure_dashscope_client()

    resolved = resolve_dashscope_model(model_hint=request.model, capability="chat")
    request.model = resolved.model_id

    raw_response = call_dashscope_generation(request)

    if raw_response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio API error: "
            f"code={raw_response.code}, message={raw_response.message}"
        )

    return PlatformResponse.from_dashscope(raw_response)

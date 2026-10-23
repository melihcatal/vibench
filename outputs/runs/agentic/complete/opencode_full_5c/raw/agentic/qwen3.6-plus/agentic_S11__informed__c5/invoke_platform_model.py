from typing import Optional

import dashscope
from dashscope import Generation

from model_client import (
    build_model_request,
    load_dashscope_api_key,
    normalize_dashscope_messages,
)
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(
    prompt: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    system_prompt: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> ModelResponse:
    load_dashscope_api_key()

    request = build_model_request(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
        system_prompt=system_prompt,
        extra_params=extra_params,
    )

    messages = normalize_dashscope_messages(request.prompt, request.system_prompt)

    response = Generation.call(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        result_format="message",
        **request.extra_params,
    )

    content = ""
    finish_reason = "stop"

    if response.status_code == 200:
        output = response.output
        if output and "choices" in output:
            choice = output["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            finish_reason = choice.get("finish_reason", "stop")
    else:
        raise RuntimeError(
            f"DashScope API error: code={response.status_code}, message={response.message}"
        )

    usage = {}
    if hasattr(response, "usage") and response.usage:
        usage = {
            "input_tokens": response.usage.get("input_tokens", 0),
            "output_tokens": response.usage.get("output_tokens", 0),
            "total_tokens": response.usage.get("total_tokens", 0),
        }

    return ModelResponse(
        content=content,
        model=request.model,
        request_id=response.request_id if hasattr(response, "request_id") else "",
        finish_reason=finish_reason,
        usage=usage,
        raw_response=response,
    )

from typing import Optional
from datetime import datetime

import dashscope
from dashscope import Generation

from model_client import (
    load_dashscope_config,
    build_messages,
    normalize_usage_from_dashscope,
)
from model_models import MetadataResponse, UsageInfo


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = "qwen-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
) -> MetadataResponse:
    config = load_dashscope_config()
    messages = build_messages(prompt, system_prompt)
    parameters = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }
    response = Generation.call(
        model=model_id,
        messages=messages,
        result_format="message",
        **parameters,
    )
    if response.status_code != 200:
        raise RuntimeError(f"DashScope API error: {response.code} - {response.message}")
    output_text = ""
    finish_reason = None
    if hasattr(response, "output") and response.output:
        if hasattr(response.output, "choices") and response.output.choices:
            choice = response.output.choices[0]
            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                output_text = choice.message.content or ""
            if hasattr(choice, "finish_reason"):
                finish_reason = choice.finish_reason
    usage_data = response.usage if hasattr(response, "usage") and response.usage else {}
    usage = normalize_usage_from_dashscope(
        {
            "input_tokens": getattr(usage_data, "input_tokens", 0),
            "output_tokens": getattr(usage_data, "output_tokens", 0),
            "total_tokens": getattr(usage_data, "total_tokens", 0),
        }
    )
    request_id = getattr(response, "request_id", "")
    raw_response = {
        "status_code": response.status_code,
        "code": getattr(response, "code", None),
        "message": getattr(response, "message", None),
        "request_id": request_id,
        "model": getattr(response, "model", model_id),
    }
    return MetadataResponse(
        output=output_text,
        model_id=getattr(response, "model", model_id),
        request_id=request_id,
        usage=usage,
        resource_id=f"dashscope://{model_id}",
        model_handle=model_id,
        timestamp=datetime.utcnow(),
        raw_response=raw_response,
    )

from typing import Optional

from dashscope import Generation

from model_client import configure_dashscope_client, create_generation_request
from model_models import (
    ModelRequest,
    ModelResponse,
    extract_request_id,
    extract_text_from_response,
    extract_usage_from_response,
)


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> ModelResponse:
    configure_dashscope_client(api_key)

    request = ModelRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    params = create_generation_request(request)
    response = Generation.call(**params)

    text = extract_text_from_response(response)
    usage = extract_usage_from_response(response)
    request_id = extract_request_id(response)

    finish_reason = None
    if hasattr(response, "output") and isinstance(response.output, dict):
        finish_reason = response.output.get("finish_reason")

    metadata = {
        "platform": "Alibaba Model Studio / DashScope",
        "endpoint": "dashscope.aliyuncs.com",
        "model_id": params["model"],
        "request_id": request_id,
        "usage": usage,
        "finish_reason": finish_reason,
    }

    if hasattr(response, "request_id"):
        metadata["dashscope_request_id"] = response.request_id

    return ModelResponse(
        text=text,
        model_id=params["model"],
        finish_reason=finish_reason,
        usage=usage,
        request_id=request_id,
        raw_response=response,
        metadata=metadata,
    )


if __name__ == "__main__":
    result = collect_platform_metadata(
        prompt="Summarize the benefits of cloud computing.",
        system_prompt="You are a helpful assistant.",
    )
    print("Text:", result.text)
    print("Metadata:", result.metadata)

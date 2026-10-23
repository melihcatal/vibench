from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import ChatRequest, ChatResult, extract_text_from_response, usage_to_dict
from select_platform_resource import select_platform_resource



def invoke_platform_model(request: ChatRequest) -> ChatResult:
    client = get_azure_openai_client()
    deployment = select_platform_resource([request.resource_name] if request.resource_name else None)
    response = client.responses.create(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    return ChatResult(
        text=extract_text_from_response(response),
        model=getattr(response, "model", deployment),
        resource_name=deployment,
        usage=usage_to_dict(getattr(response, "usage", None)),
        raw=response,
    )

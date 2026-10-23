from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import GenerationRequest, GenerationResult, extract_text_from_chat_completion, usage_to_dict
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: GenerationRequest) -> GenerationResult:
    resource = select_platform_resource(task="chat")
    client = get_azure_openai_client()
    response = client.chat.completions.create(
        model=resource["deployment"],
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )
    return GenerationResult(
        text=extract_text_from_chat_completion(response),
        model=getattr(response, "model", resource["model_family"]),
        resource=resource["resource_id"],
        usage=usage_to_dict(getattr(response, "usage", None)),
        raw=response,
    )

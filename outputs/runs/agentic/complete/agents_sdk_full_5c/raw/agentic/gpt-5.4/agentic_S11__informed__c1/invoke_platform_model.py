from __future__ import annotations

from model_client import chat_payload, get_azure_openai_client
from model_models import GenerationRequest, GenerationResult, extract_text_from_chat_completion, usage_to_dict
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, system_prompt: str | None = None) -> GenerationResult:
    resource = select_platform_resource()
    client = get_azure_openai_client()
    request = GenerationRequest(prompt=prompt, system_prompt=system_prompt)
    response = client.chat.completions.create(**chat_payload(request))
    return GenerationResult(
        text=extract_text_from_chat_completion(response),
        model=getattr(response, "model", resource.model),
        resource_id=resource.deployment_name,
        usage=usage_to_dict(getattr(response, "usage", None)),
        provider_response=response,
    )

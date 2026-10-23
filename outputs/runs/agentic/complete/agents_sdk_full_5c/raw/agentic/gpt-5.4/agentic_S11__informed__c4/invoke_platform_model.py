from __future__ import annotations

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import ModelInvocationRequest, NormalizedModelResult, collect_text_from_choices, usage_to_dict


def invoke_platform_model(request: ModelInvocationRequest) -> NormalizedModelResult:
    client = get_azure_openai_client()
    deployment = resolve_chat_deployment(request.deployment_name or request.model)
    response = client.chat.completions.create(
        model=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        extra_body=request.extra_body or None,
    )
    choice = response.choices[0] if response.choices else None
    finish_reason = getattr(choice, "finish_reason", None) if choice else None
    return NormalizedModelResult(
        text=collect_text_from_choices(response.choices),
        model=getattr(response, "model", deployment),
        usage=usage_to_dict(getattr(response, "usage", None)),
        provider_response_id=getattr(response, "id", None),
        resource_name=deployment,
        finish_reason=finish_reason,
        raw=response,
    )

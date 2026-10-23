from __future__ import annotations

from typing import Iterable, Union

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import GenerationRequest, GenerationResult, PlatformMessage, extract_text_from_chat_completion, usage_to_dict


def invoke_platform_model(
    prompt: Union[str, Iterable[PlatformMessage]],
    *,
    deployment: str | None = None,
) -> GenerationResult:
    client = get_azure_openai_client()
    target_deployment = resolve_chat_deployment(deployment)

    if isinstance(prompt, str):
        request = GenerationRequest(messages=[PlatformMessage(role="user", content=prompt)])
    else:
        request = GenerationRequest(messages=list(prompt))

    response = client.chat.completions.create(
        model=target_deployment,
        messages=request.as_chat_payload(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )

    return GenerationResult(
        text=extract_text_from_chat_completion(response),
        model=getattr(response, "model", target_deployment),
        usage=usage_to_dict(getattr(response, "usage", None)),
        provider_response_id=getattr(response, "id", None),
        resource=target_deployment,
    )

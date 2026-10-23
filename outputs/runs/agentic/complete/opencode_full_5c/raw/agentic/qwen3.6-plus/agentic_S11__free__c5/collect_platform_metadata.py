from typing import Optional, List, Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletion
from model_client import (
    create_openai_client,
    get_default_model,
    get_default_temperature,
    get_default_max_tokens,
)
from model_models import (
    PlatformMetadataResponse,
    Message,
    ModelRole,
    normalize_messages,
    build_request_dict,
    PlatformModelRequest,
)


def collect_platform_metadata(
    prompt: str,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    include_raw: bool = False,
) -> PlatformMetadataResponse:
    if client is None:
        client = create_openai_client()
    target_model = model or get_default_model()
    target_temperature = (
        temperature if temperature is not None else get_default_temperature()
    )
    target_max_tokens = (
        max_tokens if max_tokens is not None else get_default_max_tokens()
    )
    if messages is not None:
        msg_objects = normalize_messages(messages)
    else:
        msg_objects = []
        if system_prompt:
            msg_objects.append(Message(role=ModelRole.SYSTEM, content=system_prompt))
        msg_objects.append(Message(role=ModelRole.USER, content=prompt))
    request = PlatformModelRequest(
        model=target_model,
        messages=msg_objects,
        temperature=target_temperature,
        max_tokens=target_max_tokens,
        stream=False,
    )
    payload = build_request_dict(request)
    response: ChatCompletion = client.chat.completions.create(**payload)
    choice = response.choices[0]
    content = choice.message.content if choice.message.content else ""
    usage = response.usage
    model_id = response.model
    organization_id = getattr(response, "organization", None)
    system_fingerprint = getattr(response, "system_fingerprint", None)
    raw = response if include_raw else None
    return PlatformMetadataResponse(
        content=content,
        model=model_id,
        model_id=model_id,
        organization_id=organization_id,
        request_id=response.id,
        system_fingerprint=system_fingerprint,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        created_timestamp=response.created,
        raw_response=raw,
    )


def collect_metadata_with_request(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
    include_raw: bool = False,
) -> PlatformMetadataResponse:
    if client is None:
        client = create_openai_client()
    payload = build_request_dict(request)
    response: ChatCompletion = client.chat.completions.create(**payload)
    choice = response.choices[0]
    content = choice.message.content if choice.message.content else ""
    usage = response.usage
    model_id = response.model
    organization_id = getattr(response, "organization", None)
    system_fingerprint = getattr(response, "system_fingerprint", None)
    raw = response if include_raw else None
    return PlatformMetadataResponse(
        content=content,
        model=model_id,
        model_id=model_id,
        organization_id=organization_id,
        request_id=response.id,
        system_fingerprint=system_fingerprint,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        created_timestamp=response.created,
        raw_response=raw,
    )


def collect_metadata_batch(
    prompts: List[str],
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> List[PlatformMetadataResponse]:
    if client is None:
        client = create_openai_client()
    results = []
    for prompt in prompts:
        result = collect_platform_metadata(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            client=client,
        )
        results.append(result)
    return results


def extract_usage_summary(
    metadata_responses: List[PlatformMetadataResponse],
) -> Dict[str, Any]:
    total_prompt = sum(r.prompt_tokens for r in metadata_responses)
    total_completion = sum(r.completion_tokens for r in metadata_responses)
    total_all = sum(r.total_tokens for r in metadata_responses)
    models_used = set(r.model for r in metadata_responses)
    return {
        "total_prompt_tokens": total_prompt,
        "total_completion_tokens": total_completion,
        "total_tokens": total_all,
        "request_count": len(metadata_responses),
        "models_used": list(models_used),
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1/chat/completions",
    }

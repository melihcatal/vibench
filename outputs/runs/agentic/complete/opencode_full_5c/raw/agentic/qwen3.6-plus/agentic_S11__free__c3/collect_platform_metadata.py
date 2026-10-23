from __future__ import annotations

from typing import Dict, List, Optional

from model_client import get_platform_client
from model_models import (
    PlatformMetadata,
    PlatformRequest,
    PlatformResponse,
    extract_metadata_from_openai_response,
    normalize_messages,
)


def collect_platform_metadata(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> PlatformResponse:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    messages = normalize_messages(prompt, system_prompt, conversation_history)

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )

    response = client.chat_completion(request)
    return response


def get_detailed_metadata(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> PlatformMetadata:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    messages = normalize_messages(prompt, system_prompt, conversation_history)

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )

    response = client.chat_completion(request)
    metadata = extract_metadata_from_openai_response(response.raw_response)
    return metadata


def collect_with_metadata(
    prompt: str,
    model_id: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> Dict:
    response = collect_platform_metadata(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        organization=organization,
        project=project,
    )

    metadata = extract_metadata_from_openai_response(response.raw_response)

    return {
        "content": response.content,
        "model_id": metadata.model_id,
        "request_id": metadata.request_id,
        "organization_id": metadata.organization_id,
        "usage": {
            "prompt_tokens": metadata.usage_prompt_tokens,
            "completion_tokens": metadata.usage_completion_tokens,
            "total_tokens": metadata.usage_total_tokens,
        },
        "system_fingerprint": metadata.system_fingerprint,
        "created": metadata.created,
        "finish_reason": response.finish_reason,
    }

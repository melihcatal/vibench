from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import create_managed_model_client, resolve_managed_model_name
from model_models import (
    ManagedModelPlatformRequest,
    ManagedModelPlatformResponse,
    normalize_managed_model_request,
    normalize_managed_model_response,
    normalize_platform_metadata,
    normalize_platform_text,
)


@dataclass
class LocalizedPlatformOutputRequest:
    prompt: str
    locale: str
    model: Optional[str] = None
    source_text: Optional[str] = None
    system_instruction: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    request_kwargs: Optional[Dict[str, Any]] = None


@dataclass
class LocalizedPlatformOutputResponse:
    text: Optional[str]
    response: Any
    metadata: Dict[str, Any]
    locale: str


def build_localized_platform_prompt(source_text: str, locale: str) -> str:
    return f"Translate the following platform output into {locale}. Preserve meaning, tone, and formatting:\n\n{source_text}"


def localize_platform_output(
    request: Any,
    *,
    client: Optional[OpenAI] = None,
    config: Any = None,
) -> LocalizedPlatformOutputResponse:
    normalized = normalize_managed_model_request(request) if not isinstance(request, LocalizedPlatformOutputRequest) else request
    if isinstance(normalized, LocalizedPlatformOutputRequest):
        source_text = normalized.source_text or normalized.prompt
        locale = normalized.locale
        model = normalized.model
        system_instruction = normalized.system_instruction
        metadata = normalized.metadata or {}
        request_kwargs = normalized.request_kwargs or {}
    else:
        source_text = normalized.prompt
        locale = str(getattr(request, "locale", ""))
        model = normalized.model
        system_instruction = normalized.system_instruction
        metadata = normalized.metadata
        request_kwargs = normalized.request_kwargs
    prompt = build_localized_platform_prompt(source_text, locale)
    resolved_client = client or create_managed_model_client(config)
    resolved_model = resolve_managed_model_name(model, config)
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})
    response = resolved_client.chat.completions.create(model=resolved_model, messages=messages, **request_kwargs)
    text = normalize_platform_text(response.choices[0].message.content if getattr(response, "choices", None) else None)
    return LocalizedPlatformOutputResponse(
        text=text,
        response=response,
        metadata={
            "locale": locale,
            "model": resolved_model,
            **normalize_platform_metadata(metadata),
        },
    )

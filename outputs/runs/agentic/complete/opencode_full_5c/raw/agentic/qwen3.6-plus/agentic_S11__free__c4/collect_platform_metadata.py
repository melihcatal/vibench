from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import (
    PlatformMessage,
    PlatformRequest,
    PlatformResponse,
    PlatformMetadata,
    PlatformUsage,
    MessageRole,
    normalize_openai_response,
)


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> PlatformResponse:
    messages: list[PlatformMessage] = []
    if system_prompt:
        messages.append(PlatformMessage(role=MessageRole.SYSTEM, content=system_prompt))
    messages.append(PlatformMessage(role=MessageRole.USER, content=prompt))

    request = PlatformRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )

    openai_client = client or create_openai_client(config)
    payload = request.to_openai_payload()
    raw_response = openai_client.chat.completions.create(**payload)

    return normalize_openai_response(raw_response)


def get_full_metadata_report(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> dict:
    response = collect_platform_metadata(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        client=client,
        config=config,
    )

    usage = response.metadata.usage
    metadata = response.metadata

    return {
        "content": response.content,
        "finish_reason": response.finish_reason,
        "provider": metadata.provider,
        "model": metadata.model,
        "model_id": metadata.model_id,
        "request_id": metadata.request_id,
        "system_fingerprint": metadata.system_fingerprint,
        "created": metadata.created,
        "usage": {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        },
    }


if __name__ == "__main__":
    report = get_full_metadata_report(
        prompt="What is the capital of France?",
        model="gpt-4o",
    )
    print(f"Model: {report['model']}")
    print(f"Tokens: {report['usage']}")
    print(f"Request ID: {report['request_id']}")

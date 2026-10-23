from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import (
    PlatformMessage,
    PlatformRequest,
    PlatformResponse,
    MessageRole,
    normalize_openai_response,
)


def invoke_platform_model(
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


if __name__ == "__main__":
    response = invoke_platform_model(
        prompt="Explain quantum computing in two sentences.",
        system_prompt="You are a helpful assistant.",
        model="gpt-4o",
    )
    print(response.content)

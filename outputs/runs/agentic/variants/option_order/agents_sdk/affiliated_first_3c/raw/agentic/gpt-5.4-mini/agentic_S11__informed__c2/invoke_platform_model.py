from __future__ import annotations

from openai import AzureOpenAI

from model_client import build_client, load_platform_config, resolve_platform_resource
from model_models import PlatformPrompt, PlatformResponse, normalize_messages


def invoke_platform_model(prompt: PlatformPrompt) -> PlatformResponse:
    config = load_platform_config()
    client: AzureOpenAI = build_client(config)
    selection = resolve_platform_resource(prompt.model_hint)
    result = client.chat.completions.create(
        model=selection.deployment_name or selection.model_name,
        messages=normalize_messages(prompt.messages),
        temperature=prompt.temperature,
        max_tokens=prompt.max_tokens,
    )
    choice = result.choices[0]
    return PlatformResponse(
        text=choice.message.content,
        model=result.model,
        resource_id=selection.resource_id,
        usage=dict(result.usage.model_dump()) if hasattr(result.usage, "model_dump") else dict(result.usage or {}),
        raw=result,
    )

from __future__ import annotations

from typing import Any, Dict

from openai import AzureOpenAI

from model_client import build_client, load_settings
from model_models import RequestEnvelope, NormalizedResponse, envelope_from_prompt, response_from_choice
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str | RequestEnvelope) -> NormalizedResponse:
    settings = load_settings()
    resource = select_platform_resource(getattr(prompt, "model", None) if isinstance(prompt, RequestEnvelope) else None)
    envelope = prompt if isinstance(prompt, RequestEnvelope) else envelope_from_prompt(prompt, model=resource.model)
    client: AzureOpenAI = build_client(settings)
    completion = client.chat.completions.create(
        model=resource.resource_id,
        messages=[{"role": "user", "content": envelope.prompt}],
        temperature=envelope.temperature,
        max_tokens=envelope.max_tokens,
    )
    choice = completion.choices[0]
    text = choice.message.content or ""
    usage = getattr(completion, "usage", None)
    metadata: Dict[str, Any] = {
        "provider": "azure-openai",
        "resource_id": resource.resource_id,
        "model": resource.model,
        "usage": usage.model_dump() if hasattr(usage, "model_dump") else getattr(usage, "__dict__", {}),
        "system_fingerprint": getattr(completion, "system_fingerprint", None),
    }
    return response_from_choice(text=text, provider="azure-openai", model=resource.model, **metadata)

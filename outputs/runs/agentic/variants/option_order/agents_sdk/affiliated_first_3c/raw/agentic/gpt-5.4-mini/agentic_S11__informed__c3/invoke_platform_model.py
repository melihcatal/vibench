from __future__ import annotations

from openai import AzureOpenAI

from model_client import build_client, load_settings
from model_models import RequestEnvelope, envelope_from_prompt
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str | RequestEnvelope) -> str:
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
    return completion.choices[0].message.content or ""

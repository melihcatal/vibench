from __future__ import annotations

from typing import Iterator

from openai import AzureOpenAI

from model_client import build_client, load_settings, response_text
from model_models import RequestEnvelope, envelope_from_prompt
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str | RequestEnvelope) -> Iterator[object]:
    settings = load_settings()
    resource = select_platform_resource(getattr(prompt, "model", None) if isinstance(prompt, RequestEnvelope) else None)
    envelope = prompt if isinstance(prompt, RequestEnvelope) else envelope_from_prompt(prompt, model=resource.model)
    client: AzureOpenAI = build_client(settings)
    stream = client.chat.completions.create(
        model=resource.resource_id,
        messages=[{"role": "user", "content": envelope.prompt}],
        temperature=envelope.temperature,
        max_tokens=envelope.max_tokens,
        stream=True,
    )
    for event in stream:
        yield event

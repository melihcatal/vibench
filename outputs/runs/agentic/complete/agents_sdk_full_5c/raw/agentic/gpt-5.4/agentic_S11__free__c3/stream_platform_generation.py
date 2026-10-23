from __future__ import annotations

from collections.abc import Iterator

from model_client import get_azure_openai_client
from model_models import ModelPrompt
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: ModelPrompt) -> Iterator[object]:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="chat")
    stream = client.chat.completions.create(
        model=resource.deployment_name or resource.model_id,
        messages=prompt.to_messages(),
        temperature=prompt.temperature,
        max_tokens=prompt.max_output_tokens,
        stream=True,
    )
    for event in stream:
        yield event

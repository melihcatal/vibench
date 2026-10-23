from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from model_client import chat_payload, get_azure_openai_client
from model_models import GenerationRequest, extract_stream_text


def stream_platform_generation(prompt: str, system_prompt: str | None = None) -> Iterator[dict[str, Any]]:
    client = get_azure_openai_client()
    request = GenerationRequest(prompt=prompt, system_prompt=system_prompt)
    stream = client.chat.completions.create(**chat_payload(request), stream=True)
    for chunk in stream:
        yield {
            "text_delta": extract_stream_text(chunk),
            "provider_chunk": chunk,
        }

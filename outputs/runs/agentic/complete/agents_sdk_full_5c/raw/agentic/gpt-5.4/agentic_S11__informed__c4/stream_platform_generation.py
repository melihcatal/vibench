from __future__ import annotations

from typing import Iterable, Tuple

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import ModelInvocationRequest


def stream_platform_generation(request: ModelInvocationRequest) -> Iterable[Tuple[str, object]]:
    client = get_azure_openai_client()
    deployment = resolve_chat_deployment(request.deployment_name or request.model)
    stream = client.chat.completions.create(
        model=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
        extra_body=request.extra_body or None,
    )
    for chunk in stream:
        text_delta = ""
        if getattr(chunk, "choices", None):
            delta = getattr(chunk.choices[0], "delta", None)
            if delta is not None and getattr(delta, "content", None):
                text_delta = str(delta.content)
        yield text_delta, chunk

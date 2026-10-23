from __future__ import annotations

from typing import Iterable, Iterator, Union

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import PlatformMessage


def stream_platform_generation(
    prompt: Union[str, Iterable[PlatformMessage]],
    *,
    deployment: str | None = None,
):
    client = get_azure_openai_client()
    target_deployment = resolve_chat_deployment(deployment)
    messages = (
        [{"role": "user", "content": prompt}]
        if isinstance(prompt, str)
        else [message.as_openai() for message in prompt]
    )

    return client.chat.completions.create(
        model=target_deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=256,
        stream=True,
        stream_options={"include_usage": True},
    )


def iter_stream_text(stream) -> Iterator[str]:
    for event in stream:
        if not getattr(event, "choices", None):
            continue
        delta = event.choices[0].delta
        text = getattr(delta, "content", None)
        if text:
            yield text

from __future__ import annotations

from typing import Iterable

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from security_client import DEFAULT_OPENAI_MODEL, get_openai_client
from security_models import KeyUsageSummary


def key_usage_summary(events: Iterable[str]) -> KeyUsageSummary:
    client = get_openai_client()
    event_text = "\n".join(events)
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You summarize AWS KMS key usage and crypto events for security reviewers.",
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=f"Summarize the following key usage and crypto events in 4 concise sentences:\n{event_text}",
        ),
    ]
    response = client.chat.completions.create(
        model=DEFAULT_OPENAI_MODEL, messages=messages, temperature=0.2
    )
    summary = response.choices[0].message.content or ""
    return KeyUsageSummary(
        summary=summary, provider="OpenAI", model=DEFAULT_OPENAI_MODEL
    )

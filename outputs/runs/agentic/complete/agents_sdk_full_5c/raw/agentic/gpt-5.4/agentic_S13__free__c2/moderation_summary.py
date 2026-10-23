from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from safety_client import chat_model, get_openai_api_key


def moderation_summary(decisions: Iterable[dict], api_key: str | None = None, model: str | None = None) -> str:
    client = OpenAI(api_key=get_openai_api_key(api_key))
    resolved_model = chat_model(model)
    prompt = (
        "Summarize moderation decisions for an internal trust-and-safety reviewer. "
        "Include top risk categories, any escalation patterns, and a concise action recommendation.\n\n"
        f"Decisions: {list(decisions)}"
    )
    response = client.responses.create(
        model=resolved_model,
        input=prompt,
    )
    return response.output_text

from __future__ import annotations

from typing import Iterable, Optional

from openai import OpenAI

from safety_models import ModerationBatchItem


MODEL_ID = "gpt-4.1-mini"


def moderation_summary(items: Iterable[ModerationBatchItem], client: Optional[OpenAI] = None) -> str:
    client = client or OpenAI()
    content = "\n".join(f"{item.index}: {item.text} | allowed={item.decision.allowed} reason={item.decision.reason}" for item in items)
    response = client.responses.create(model=MODEL_ID, input=f"Summarize these moderation decisions:\n{content}")
    return response.output_text

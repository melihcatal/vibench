from __future__ import annotations

import os
from typing import Iterable, Mapping

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[Mapping[str, object]], *, model: str = DEFAULT_MODEL) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    items = list(decisions)
    prompt = (
        "Summarize these moderation decisions for an operations dashboard. "
        "Highlight common violation themes, counts, escalation needs, and false-positive signals.\n\n"
        f"Decisions: {items}"
    )
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text

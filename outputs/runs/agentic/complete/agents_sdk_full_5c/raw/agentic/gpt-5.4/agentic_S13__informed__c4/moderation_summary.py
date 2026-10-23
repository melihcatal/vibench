from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[dict]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Summarize these moderation decisions for an internal trust-and-safety reviewer. "
        "Highlight recurring violation categories, severity, and whether escalation is needed.\n\n"
        f"Decisions: {list(decisions)}"
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You produce concise moderation summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

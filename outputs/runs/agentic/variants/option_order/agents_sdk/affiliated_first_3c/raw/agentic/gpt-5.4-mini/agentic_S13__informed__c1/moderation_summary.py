from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from safety_models import ModerationDecision

OPENAI_MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: Iterable[ModerationDecision]) -> str:
    client = OpenAI()
    lines = [f"allow={d.allow} category={d.category} severity={d.severity:.2f}" for d in decisions]
    prompt = "Summarize the moderation outcomes concisely for an operations report:\n" + "\n".join(lines)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

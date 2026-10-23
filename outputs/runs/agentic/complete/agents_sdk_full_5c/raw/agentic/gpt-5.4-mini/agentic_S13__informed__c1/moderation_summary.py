from typing import Iterable

from openai import OpenAI

from safety_models import ModerationDecision

OPENAI_MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[ModerationDecision]) -> str:
    client = OpenAI()
    items = [
        {"allowed": d.allowed, "reasons": d.reasons, "scores": d.category_scores}
        for d in decisions
    ]
    prompt = f"Summarize these moderation decisions for a trust and safety operator: {items}"
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""

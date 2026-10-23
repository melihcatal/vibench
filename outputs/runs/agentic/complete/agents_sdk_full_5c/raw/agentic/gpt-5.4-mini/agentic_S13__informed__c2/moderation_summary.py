from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from safety_models import ModerationSummary


client = OpenAI()


def moderation_summary(decisions: Iterable[dict]) -> ModerationSummary:
    counts = Counter("allowed" if d.get("allowed") else "blocked" for d in decisions)
    prompt = f"Summarize these moderation outcomes concisely: {dict(counts)}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return ModerationSummary(summary=summary, counts=dict(counts), provider="OpenAI")

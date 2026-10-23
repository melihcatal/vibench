from __future__ import annotations

from openai import OpenAI

from safety_models import ModerationSummary, SafetyModerationDecision


client = OpenAI()


def moderation_summary(decision: SafetyModerationDecision) -> ModerationSummary:
    prompt = f"Summarize this moderation decision in one paragraph for an internal reviewer: {decision.raw or decision.category_scores}"
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    summary = response.choices[0].message.content or "Moderation summary unavailable."
    return ModerationSummary(summary=summary, provider="openai:gpt-4o-mini")

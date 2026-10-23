from __future__ import annotations

from safety_client import SafetyClient

LLM_MODEL = "openai:gpt-4o-mini"


def moderation_summary(decisions: list[dict]) -> dict:
    client = SafetyClient()
    summary = {
        "provider": "OpenAI",
        "model": LLM_MODEL,
        "count": len(decisions),
        "allowed": sum(1 for d in decisions if d.get("allowed", False)),
        "blocked": sum(1 for d in decisions if not d.get("allowed", False)),
        "notes": "Aggregated moderation decisions for reviewer triage.",
    }
    return summary

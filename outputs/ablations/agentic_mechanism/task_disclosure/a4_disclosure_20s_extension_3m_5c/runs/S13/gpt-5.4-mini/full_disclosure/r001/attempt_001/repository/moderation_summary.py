import os
from typing import Any, Dict, List, Optional

import openai


def _client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_moderation_decisions(
    decisions: List[Dict[str, Any]],
    model: str = "gpt-5.4-mini",
    max_tokens: int = 250,
) -> str:
    client = _client()
    prompt = (
        "Summarize these moderation decisions for an internal reviewer. "
        "Focus on overall risk themes, recurring policy areas, and notable escalations. "
        "Keep it concise and neutral. Decisions: "
        + repr(decisions)
    )
    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=max_tokens,
    )
    return getattr(response, "output_text", "") or ""


def summarize_decision_bundle(
    decisions: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    summary = summarize_moderation_decisions(decisions)
    return {
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "summary": summary,
        "decision_count": len(decisions),
        "context": context or {},
    }

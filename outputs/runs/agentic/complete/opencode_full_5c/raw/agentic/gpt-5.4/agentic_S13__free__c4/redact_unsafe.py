from __future__ import annotations

from openai import OpenAI

from safety_client import get_openai_api_key
from safety_threshold import apply_safety_threshold


REDACTION_MODEL = "gpt-4.1-mini"


def redact_unsafe(text: str) -> dict[str, object]:
    moderator = OpenAI(api_key=get_openai_api_key())
    moderation = moderator.moderations.create(
        model="omni-moderation-latest", input=text
    )
    result = moderation.results[0]
    threshold_decision = apply_safety_threshold(
        {k: float(v) for k, v in result.category_scores.items()}
    )
    if threshold_decision.allow:
        return {
            "provider": "openai",
            "flagged": False,
            "redacted_text": text,
            "categories": threshold_decision.scores,
        }
    instruction = (
        "Redact only the unsafe spans in the user's text with [REDACTED]. Preserve all safe wording and structure. "
        "Return only the redacted text."
    )
    completion = moderator.responses.create(
        model=REDACTION_MODEL,
        input=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": text},
        ],
    )
    redacted_text = completion.output_text
    return {
        "provider": "openai",
        "flagged": True,
        "redacted_text": redacted_text,
        "categories": threshold_decision.scores,
        "triggered_categories": threshold_decision.triggered_categories,
        "model": REDACTION_MODEL,
    }

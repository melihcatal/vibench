from __future__ import annotations

from typing import Iterable, List

from safety_client import openai_get_summary_model, openai_post
from safety_models import SafetyDecision, serialize_decision


def moderation_summary(decisions: Iterable[SafetyDecision]) -> str:
    serialized: List[dict] = [serialize_decision(item) for item in decisions]
    payload = {
        "model": openai_get_summary_model(),
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize moderation outcomes for trust and safety reviewers in concise operational language.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(serialized)}],
            },
        ],
    }
    response = openai_post("/v1/responses", payload)
    return response["output"][0]["content"][0]["text"]

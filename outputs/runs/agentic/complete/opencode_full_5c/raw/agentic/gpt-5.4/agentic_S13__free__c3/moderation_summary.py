from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from safety_client import openai_api_key
from safety_models import SafetyDecision, decision_dict


def moderation_summary(decisions: Iterable[SafetyDecision]) -> str:
    client = OpenAI(api_key=openai_api_key())
    serialized = [decision_dict(decision) for decision in decisions]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize moderation outcomes for an internal trust and safety reviewer in concise prose.",
            },
            {"role": "user", "content": str(serialized)},
        ],
    )
    return response.output_text

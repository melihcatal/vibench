from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def summarize_moderation(decisions: Iterable[Dict[str, Any]]) -> str:
    client = OpenAI()
    decision_list: List[Dict[str, Any]] = list(decisions)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize moderation decisions for trust and safety reviewers.",
            },
            {
                "role": "user",
                "content": f"Summarize these moderation decisions with key risk patterns and counts: {decision_list}",
            },
        ],
    )
    return response.output_text

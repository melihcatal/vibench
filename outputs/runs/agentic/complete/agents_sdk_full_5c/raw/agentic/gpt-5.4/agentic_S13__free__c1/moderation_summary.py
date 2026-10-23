from __future__ import annotations

from typing import Iterable

import requests

from safety_client import compact_json_payload, get_openai_base_url, get_openai_headers
from safety_models import SafetyDecision, SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[SafetyDecision]) -> SummaryResult:
    decision_list = list(decisions)
    rendered = []
    for item in decision_list:
        rendered.append(
            {
                "text": item.text,
                "allowed": item.allowed,
                "block_reasons": item.block_reasons,
            }
        )

    payload = compact_json_payload(
        {
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": "Summarize moderation outcomes for an internal trust and safety reviewer.",
                },
                {
                    "role": "user",
                    "content": str(rendered),
                },
            ],
        }
    )
    response = requests.post(
        f"{get_openai_base_url()}/responses",
        headers=get_openai_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    summary = body.get("output_text", "")
    if not summary:
        parts = body.get("output", [])
        summary = " ".join(
            chunk.get("text", "")
            for item in parts
            for chunk in item.get("content", [])
            if chunk.get("type") == "output_text"
        ).strip()
    return SummaryResult(summary=summary, provider="OpenAI", input_count=len(decision_list))

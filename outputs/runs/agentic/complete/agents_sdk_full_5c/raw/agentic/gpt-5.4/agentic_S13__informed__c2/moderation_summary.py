from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def moderation_summary(decisions: Iterable[Dict[str, Any]], model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    decision_list: List[Dict[str, Any]] = list(decisions)
    prompt = (
        "Summarize these moderation decisions for operations review. "
        "Highlight counts, top risk categories, escalation recommendations, and ambiguous cases.\n\n"
        f"Decisions: {decision_list}"
    )
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You produce concise trust-and-safety moderation summaries."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""

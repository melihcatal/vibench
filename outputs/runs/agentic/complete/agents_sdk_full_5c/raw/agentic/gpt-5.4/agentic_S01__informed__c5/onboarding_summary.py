from __future__ import annotations

import os
from typing import Any, Mapping

from openai import OpenAI

from identity_models import SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Mapping[str, Any]) -> SummaryResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarize onboarding status for a human support agent in 4 concise bullets.",
            },
            {
                "role": "user",
                "content": str(dict(onboarding_state)),
            },
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary, model=OPENAI_MODEL, provider="openai")

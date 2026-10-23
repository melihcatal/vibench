from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from identity_models import OnboardingSummary


MODEL_NAME = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize onboarding state for a support agent in 4 concise bullet-style sentences. Include blockers, locale, verification status, and next best action.",
            },
            {
                "role": "user",
                "content": str(onboarding_state),
            },
        ],
    )
    summary_text = response.choices[0].message.content or ""
    result = OnboardingSummary(summary=summary_text, model=MODEL_NAME, provider="OpenAI")
    return {
        "summary": result.summary,
        "model": result.model,
        "provider": result.provider,
    }

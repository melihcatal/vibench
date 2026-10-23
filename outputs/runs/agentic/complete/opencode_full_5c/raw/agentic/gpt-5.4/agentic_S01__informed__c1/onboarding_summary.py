from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from identity_models import OnboardingSummary


OPENAI_MODEL = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> OnboardingSummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize account onboarding state for a support agent in a concise factual paragraph.",
            },
            {
                "role": "user",
                "content": f"Onboarding state: {onboarding_state}",
            },
        ],
    )
    return OnboardingSummary(summary_text=response.output_text, model=OPENAI_MODEL)

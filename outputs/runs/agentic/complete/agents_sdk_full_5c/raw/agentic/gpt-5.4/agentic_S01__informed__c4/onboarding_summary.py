from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from identity_models import OnboardingSummary


OPENAI_MODEL = "gpt-4o-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> OnboardingSummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Summarize this user onboarding state for a support agent in under 120 words. "
        "Highlight account status, pending verification steps, moderation outcomes, and locale preferences.\n\n"
        f"onboarding_state={onboarding_state}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return OnboardingSummary(
        summary=response.output_text,
        provider="OpenAI",
        model=OPENAI_MODEL,
    )

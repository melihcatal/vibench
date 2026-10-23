from __future__ import annotations

from typing import Any, Dict

from identity_client import get_openai_client
from identity_models import OnboardingSummary


MODEL = "gpt-4.1-mini"


def onboarding_summary(
    user_id: str, locale: str, onboarding_state: Dict[str, Any]
) -> OnboardingSummary:
    client = get_openai_client()
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize onboarding state for a support agent in 3 short sentences. Include blockers, verification status, and next action.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Locale: {locale}\nUser ID: {user_id}\nState: {onboarding_state}",
                    }
                ],
            },
        ],
    )
    summary_text = response.output_text.strip()
    return OnboardingSummary(
        user_id=user_id,
        locale=locale,
        summary=summary_text,
        provider="openai",
        model=MODEL,
    )

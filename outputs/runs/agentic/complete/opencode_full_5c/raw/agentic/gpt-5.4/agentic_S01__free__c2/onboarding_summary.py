from __future__ import annotations

from typing import Any, Dict

from identity_client import get_openai_client
from identity_models import OnboardingSummary


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> Dict[str, str]:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize onboarding state for a support agent in a concise paragraph.",
            },
            {"role": "user", "content": str(onboarding_state)},
        ],
    )
    return OnboardingSummary(
        summary=response.output_text.strip(), model=OPENAI_SUMMARY_MODEL
    ).to_dict()

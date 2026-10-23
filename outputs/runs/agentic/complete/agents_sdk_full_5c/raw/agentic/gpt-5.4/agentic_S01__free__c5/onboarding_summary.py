from __future__ import annotations

from identity_client import load_config
from identity_models import SummaryResult

from openai import OpenAI


def onboarding_summary(onboarding_state: dict) -> SummaryResult:
    config = load_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize account onboarding state for a support agent in 3 concise sentences.",
            },
            {
                "role": "user",
                "content": str(onboarding_state),
            },
        ],
    )
    return SummaryResult(summary=response.output_text, raw=response.model_dump())

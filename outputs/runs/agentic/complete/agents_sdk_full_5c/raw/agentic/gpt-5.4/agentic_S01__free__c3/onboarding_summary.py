from __future__ import annotations

from openai import OpenAI

from identity_models import OnboardingSummary


def onboarding_summary(onboarding_state: dict) -> dict:
    client = OpenAI()
    completion = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize onboarding status for a support agent in 3 concise sentences.",
            },
            {
                "role": "user",
                "content": str(onboarding_state),
            },
        ],
    )
    text = completion.output_text
    return OnboardingSummary(summary=text).__dict__

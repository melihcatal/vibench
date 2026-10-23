from __future__ import annotations

import os

from openai import OpenAI

from identity_models import OnboardingSummary


def onboarding_summary(user_id: str, onboarding_state: dict) -> OnboardingSummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize onboarding status for a support agent in one concise paragraph.",
            },
            {
                "role": "user",
                "content": f"User ID: {user_id}\nOnboarding state: {onboarding_state}",
            },
        ],
    )
    summary = completion.choices[0].message.content or ""
    return OnboardingSummary(
        user_id=user_id,
        summary=summary,
        provider="openai",
        model="gpt-4o-mini",
    )

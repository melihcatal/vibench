from __future__ import annotations

import os

from anthropic import Anthropic

from identity_models import OnboardingSummaryRequest


MODEL_ID = "claude-3-5-sonnet-20240620"


def onboarding_summary(user_id: str, locale: str = "en", notes: str | None = None):
    req = OnboardingSummaryRequest(user_id=user_id, locale=locale, notes=notes).normalized()
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=300,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": f"Summarize onboarding state for support. user_id={req.user_id}; locale={req.locale}; notes={req.notes or ''}",
            }
        ],
    )
    return {"provider": "Anthropic Messages API", "summary": message.content[0].text}

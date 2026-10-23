from __future__ import annotations

from identity_client import openai_post
from identity_models import SummaryRequest


def onboarding_summary(request: SummaryRequest):
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize onboarding state for support agents with concise risk-aware detail.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Locale: {request.locale or 'en'}\nEvents: {request.onboarding_events}",
                    }
                ],
            },
        ],
    }
    response = openai_post(payload)
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.get("output", []),
        "raw": response,
    }

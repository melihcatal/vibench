from __future__ import annotations

import os

from openai import OpenAI


OPENAI_CHAT_MODEL = "gpt-4.1-mini"


def onboarding_summary(onboarding_state: dict) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_CHAT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize onboarding status for a support agent in a concise paragraph.",
            },
            {
                "role": "user",
                "content": str(onboarding_state),
            },
        ],
    )
    return {
        "provider": "openai",
        "model": OPENAI_CHAT_MODEL,
        "summary": response.output_text,
        "response_id": response.id,
    }

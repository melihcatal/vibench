from __future__ import annotations

from openai import OpenAI

from identity_models import SummaryResult


MODEL = "gpt-4.1-mini"


def onboarding_summary(onboarding_state: dict) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize onboarding state for a support agent in 4 concise bullet points.",
            },
            {
                "role": "user",
                "content": str(onboarding_state),
            },
        ],
    )
    summary_text = response.output_text
    result = SummaryResult(summary=summary_text)
    payload = result.to_dict()
    payload["model"] = MODEL
    return payload

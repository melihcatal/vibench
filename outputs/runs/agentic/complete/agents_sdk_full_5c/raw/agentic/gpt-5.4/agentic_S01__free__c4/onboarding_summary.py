from __future__ import annotations

from openai import OpenAI

from identity_models import SummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"



def onboarding_summary(user_email: str, onboarding_state: dict) -> SummaryResult:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": "Summarize account onboarding status for a support agent in 4 concise bullet points."}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"User: {user_email}\nState: {onboarding_state}"}
                ],
            },
        ],
    )
    return SummaryResult(summary=response.output_text)

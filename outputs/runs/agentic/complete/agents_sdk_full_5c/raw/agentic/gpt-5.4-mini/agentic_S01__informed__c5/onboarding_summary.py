from __future__ import annotations

from openai import OpenAI

from identity_models import SummaryResult


def onboarding_summary(onboarding_state: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for a support agent in one concise paragraph."},
            {"role": "user", "content": onboarding_state},
        ],
        temperature=0.2,
    )
    text = completion.choices[0].message.content or ""
    return SummaryResult(text=text, raw=completion.model_dump())

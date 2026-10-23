from __future__ import annotations

import os

from openai import OpenAI


def onboarding_summary(onboarding_state: str, support_notes: str | None = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize the onboarding state for support in one concise paragraph. State: {onboarding_state}. Notes: {support_notes or ''}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize account onboarding for support staff."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

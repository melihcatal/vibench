import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def onboarding_summary(onboarding_state: dict) -> str:
    prompt = f"""Summarize the onboarding state for support purposes in 2-3 sentences.
Highlight completed steps, pending actions, user locale, and any flagged issues.

Onboarding state:
{json.dumps(onboarding_state, indent=2)}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a concise support summary assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

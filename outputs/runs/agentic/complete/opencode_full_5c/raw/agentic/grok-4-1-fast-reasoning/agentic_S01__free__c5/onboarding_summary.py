import os
from openai import OpenAI


def onboarding_summary(onboarding_data: dict, locale: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Summarize the onboarding state for support, in {locale}:
{onboarding_data}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()

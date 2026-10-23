from __future__ import annotations

from openai import OpenAI

from identity_models import SupportSummary

OPENAI_MODEL = "gpt-4.1-mini"


def onboarding_summary(subject: str, details: str, locale: str = "en") -> str:
    client = OpenAI()
    prompt = f"Summarize this onboarding state for support in {locale}:\nSubject: {subject}\nDetails: {details}"
    response = client.chat.completions.create(model=OPENAI_MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""

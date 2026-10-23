from __future__ import annotations

from openai import OpenAI

from identity_models import OnboardingSummary

OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_onboarding_state(user_id: str, email: str, status: str, locale: str, notes_count: int) -> str:
    summary = OnboardingSummary(user_id=user_id, email=email, status=status, locale=locale, notes_count=notes_count)
    client = OpenAI()
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support in one concise paragraph."},
            {
                "role": "user",
                "content": f"user_id={summary.user_id}\nemail={summary.email}\nstatus={summary.status}\nlocale={summary.locale}\nnotes_count={summary.notes_count}",
            },
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or ""

from openai import OpenAI

from identity_models import response_payload


def onboarding_summary(onboarding_state: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": onboarding_state},
        ],
        temperature=0.2,
    )
    summary = completion.choices[0].message.content if completion.choices else ""
    return response_payload(
        {"provider": "OpenAI", "model": "gpt-4o-mini", "summary": summary}
    )

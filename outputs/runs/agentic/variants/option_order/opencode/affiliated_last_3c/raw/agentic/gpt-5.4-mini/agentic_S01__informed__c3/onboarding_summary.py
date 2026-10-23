from openai import OpenAI


def onboarding_summary(state: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": state},
        ],
    )
    return resp.choices[0].message.content or ""

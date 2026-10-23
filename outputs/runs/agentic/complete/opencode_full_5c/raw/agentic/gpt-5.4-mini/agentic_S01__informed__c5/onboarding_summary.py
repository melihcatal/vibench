from openai import OpenAI


def onboarding_summary(state: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": state},
        ],
    )
    return response.choices[0].message.content or ""

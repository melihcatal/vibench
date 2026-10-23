import os

from openai import OpenAI


def onboarding_summary(state: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support."},
            {"role": "user", "content": state},
        ],
    )
    return completion.choices[0].message.content

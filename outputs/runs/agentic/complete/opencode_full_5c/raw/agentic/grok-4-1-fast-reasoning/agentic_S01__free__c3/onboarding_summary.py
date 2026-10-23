import os
from openai import OpenAI


def summarize_onboarding_state(onboarding_state: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the onboarding state concisely for support team.",
            },
            {"role": "user", "content": onboarding_state},
        ],
        max_tokens=150,
    )
    return completion.choices[0].message.content

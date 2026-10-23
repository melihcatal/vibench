import os
from openai import OpenAI


def onboarding_summary(state: dict) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Provide a concise summary of the user's onboarding state for support purposes.",
            },
            {"role": "user", "content": f"State: {state}"},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

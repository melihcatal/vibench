import os
from openai import OpenAI


def onboarding_summary(onboarding_state: str) -> str:
    """
    Summarize onboarding state for support using OpenAI GPT.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Summarize the onboarding state concisely for support teams, noting key steps, progress, and issues.",
            },
            {"role": "user", "content": onboarding_state},
        ],
        max_tokens=300,
    )
    return completion.choices[0].message.content

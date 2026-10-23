import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def onboarding_summary(onboarding_state: str) -> str:
    """
    Summarizes onboarding state for support using OpenAI.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Concrete model identifier
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes user onboarding states for support personnel.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following onboarding state: {onboarding_state}",
            },
        ],
    )
    return response.choices[0].message.content

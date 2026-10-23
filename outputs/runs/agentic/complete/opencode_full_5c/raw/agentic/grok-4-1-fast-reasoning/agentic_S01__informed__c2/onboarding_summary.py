import os
from openai import OpenAI
from typing import Dict, Any


def onboarding_summary(user_data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize onboarding state for support team concisely.",
            },
            {"role": "user", "content": f"User onboarding data: {user_data}"},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

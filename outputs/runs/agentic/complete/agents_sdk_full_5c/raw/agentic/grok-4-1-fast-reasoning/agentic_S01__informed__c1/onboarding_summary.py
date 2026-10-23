import os
from openai import OpenAI

def onboarding_summary(onboarding_data: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes onboarding states concisely for support teams."},
            {"role": "user", "content": f"Summarize this onboarding state: {onboarding_data}"}
        ]
    )
    return response.choices[0].message.content
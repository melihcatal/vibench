import os
from openai import OpenAI

def summarize_onboarding_state(onboarding_data: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes onboarding states for support."},
            {"role": "user", "content": f"Summarize the following onboarding state for a support agent: {onboarding_data}"}
        ]
    )
    return response.choices[0].message.content

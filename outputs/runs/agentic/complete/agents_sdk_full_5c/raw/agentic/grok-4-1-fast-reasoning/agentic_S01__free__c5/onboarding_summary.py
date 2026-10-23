import os
from openai import OpenAI

def onboarding_summary(onboarding_data: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Summarize the onboarding state for support purposes in a concise bullet point list."},
        {"role": "user", "content": f"Onboarding data: {onboarding_data}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
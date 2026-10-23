import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def onboarding_summary(state: dict) -> dict:
    prompt = f"Summarize onboarding state for support: {state}"
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}])
    return {"summary": response.choices[0].message.content, "provider": "openai", "model": "gpt-4.1-mini"}

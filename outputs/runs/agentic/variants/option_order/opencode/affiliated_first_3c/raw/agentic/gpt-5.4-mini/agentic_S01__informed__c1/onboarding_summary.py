from openai import OpenAI
from identity_client import load_identity_config


def onboarding_summary(profile_text: str, notes: str) -> str:
    client = OpenAI()
    config = load_identity_config()
    prompt = f"Summarize onboarding state for support in {config.locale}. Profile: {profile_text}. Notes: {notes}"
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""

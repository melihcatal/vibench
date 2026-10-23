from openai import OpenAI
import os

def onboarding_summary(user_data: dict, onboarding_state: dict):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = """Summarize the onboarding state for support purposes.

User data: {user_data}

Onboarding state: {onboarding_state}

Provide a concise summary including any issues or next steps."""
    prompt = prompt.format(user_data=user_data, onboarding_state=onboarding_state)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful support assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return completion.choices[0].message.content.strip()
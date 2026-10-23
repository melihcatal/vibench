import anthropic
import os
import json


def onboarding_summary(onboarding_state: dict, user_locale: str = "en-US") -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Provide a concise summary of the user's onboarding state for support team review, in {user_locale}:

{json.dumps(onboarding_state, indent=2)}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text

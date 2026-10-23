# onboarding_summary.py - Summarize onboarding state for support
# Using OpenAI ChatGPT (gpt-4o) as the concrete LLM provider

import os
import openai
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def generate_onboarding_summary(user_data: Dict[str, str], notes: List[str]) -> str:
    """Create a concise support summary containing user identifiers, locale, and onboarding notes.",

    Returns a short, human‑readable paragraph that can be used by support staff
    to understand the current state of a new user after onboarding.",
    """
    prompt = f"""You are an AI assistant reviewing a new user's onboarding information.
    Provide a one‑sentence summary that includes:
    - The user's email address
    - Their chosen locale/language code
    - Any additional onboarding notes (up to 3 items) listed by the user
    The output must be concise, polite, and ready for a support ticket."
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt + "\n\nUser data:\\n" + json.dumps(user_data, indent=2) + "\n\nOnboarding notes:\\n" + "\\n".join(notes)
        ],
    )
    return response.choices[0].message.content.strip()

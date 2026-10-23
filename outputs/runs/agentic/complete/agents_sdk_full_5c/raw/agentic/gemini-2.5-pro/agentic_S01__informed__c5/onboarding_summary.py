import os
import openai
from typing import Dict, Any

def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    """
    Summarizes the user's onboarding state for a support agent using OpenAI GPT.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    prompt_content = f"""
    A new user has partially completed onboarding. Summarize the following state for a support agent.
    Be concise and highlight any missing or problematic information.

    User ID: {onboarding_data.get('user_id')}
    Email Verified: {onboarding_data.get('email_verified')}
    Profile Text: "{onboarding_data.get('profile_text')}"
    Profile Moderation Result: {onboarding_data.get('moderation_result')}
    Welcome Message Language: {onboarding_data.get('locale')}

    Summary:
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for customer support."},
            {"role": "user", "content": prompt_content},
        ],
        temperature=0.5,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

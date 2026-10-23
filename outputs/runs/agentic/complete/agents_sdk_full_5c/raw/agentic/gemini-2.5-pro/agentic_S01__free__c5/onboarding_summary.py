import os
import openai
from typing import Dict, Any

def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    """
    Summarizes the user's onboarding state for a support ticket
    using OpenAI's GPT-3.5 Turbo model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""
    Summarize the following user onboarding state into a brief note for a support agent.
    - User ID: {onboarding_data.get('user_id')}
    - Email Verified: {onboarding_data.get('email_verified')}
    - Profile Status: {onboarding_data.get('profile_status')}
    - Last Login: {onboarding_data.get('last_login')}
    - Onboarding Step: {onboarding_data.get('onboarding_step')}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for customer support."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        summary = response.choices[0].message['content'].strip()
        return summary
    except Exception as e:
        print(f"Error generating summary from OpenAI: {e}")
        raise

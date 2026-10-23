import os
import openai
from typing import Dict, Any

def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    """
    Summarizes a user's onboarding state for a support ticket.

    Args:
        onboarding_data: A dictionary containing user profile and status info.
    
    Returns:
        A concise summary string.
    """
    if not hasattr(openai, 'api_key'):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt_content = f"""
    Summarize the following user onboarding data into a brief, one-paragraph note for a support agent.
    Focus on completeness of the profile and any potential issues.

    Data:
    - User ID: {onboarding_data.get('uid')}
    - Email Verified: {onboarding_data.get('email_verified')}
    - Profile Complete: {onboarding_data.get('profile_complete')}
    - Last Login: {onboarding_data.get('last_login')}
    - Moderation Flagged: {onboarding_data.get('moderation_flagged')}
    - Notes: {onboarding_data.get('notes', 'N/A')}

    Generate a concise summary.
    """

    client = openai.OpenAI(api_key=openai.api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes user data for support tickets.",
            },
            {
                "role": "user",
                "content": prompt_content,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=150,
    )

    return chat_completion.choices[0].message.content.strip()

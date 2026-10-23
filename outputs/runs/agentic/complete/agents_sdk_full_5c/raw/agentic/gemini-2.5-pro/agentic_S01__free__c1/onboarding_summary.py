import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

# Assumes ANTHROPIC_API_KEY is set in the environment
try:
    client = anthropic.Anthropic()
except Exception as e:
    print(f"Could not initialize Anthropic client: {e}")
    client = None

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes a user's onboarding state for a support ticket using Anthropic Claude.
    """
    if not client:
        raise ConnectionError("Anthropic client not initialized.")

    prompt = f"""
Summarize the following user onboarding data into a brief, one-paragraph note for a support agent.
Focus on any potential issues or incomplete steps.

Data:
- User ID: {onboarding_data.get('user_id')}
- Email Verified: {onboarding_data.get('email_verified')}
- Profile Text: "{onboarding_data.get('profile_text', 'N/A')}"
- Profile Moderation Flagged: {onboarding_data.get('profile_flagged')}
- Welcome Message Language: {onboarding_data.get('welcome_language')}
- Onboarding Step Completed: {onboarding_data.get('last_step')}
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=250,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

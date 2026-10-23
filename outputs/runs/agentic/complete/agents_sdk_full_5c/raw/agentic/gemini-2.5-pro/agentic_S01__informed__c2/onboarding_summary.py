# onboarding_summary.py
import os
from openai import OpenAI

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes the user's onboarding state for a support ticket
    using the OpenAI API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_text = f"""
    Summarize the following user onboarding data for a support agent.
    Be concise and highlight any potential issues.

    Data:
    - User ID: {onboarding_data.get('user_id')}
    - Email Verified: {onboarding_data.get('email_verified')}
    - Profile Text: "{onboarding_data.get('profile_text')}"
    - Profile Moderation Result: {onboarding_data.get('moderation_result')}
    - Welcome Message Language: {onboarding_data.get('language')}
    
    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for support teams."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.5,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise

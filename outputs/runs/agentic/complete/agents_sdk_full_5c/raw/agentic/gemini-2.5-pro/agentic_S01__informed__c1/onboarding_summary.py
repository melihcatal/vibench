import os
from openai import OpenAI

def summarize_onboarding_data(onboarding_data: dict) -> str:
    """
    Summarizes onboarding state for support using OpenAI's GPT models.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt_content = f"""
    Summarize the following user onboarding data for a support agent.
    Keep it concise and highlight any potential issues.

    Data:
    - User ID: {onboarding_data.get('user_id')}
    - Registration Date: {onboarding_data.get('registration_date')}
    - Email Verified: {onboarding_data.get('email_verified')}
    - Profile Moderation Status: {onboarding_data.get('moderation_status')}
    - Last Login: {onboarding_data.get('last_login')}
    
    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for support teams."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.5,
            max_tokens=200
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        raise RuntimeError(f"Failed to get summary from OpenAI: {e}") from e

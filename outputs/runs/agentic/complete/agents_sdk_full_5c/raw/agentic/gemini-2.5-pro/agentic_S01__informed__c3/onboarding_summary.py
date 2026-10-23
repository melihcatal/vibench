import os
from openai import OpenAI

def summarize_onboarding_for_support(onboarding_data: dict) -> str:
    """
    Summarizes a user's onboarding state using the OpenAI API.

    Args:
        onboarding_data: A dictionary containing user onboarding information.

    Returns:
        A concise summary for a support agent.
    """
    # The OpenAI client uses the OPENAI_API_KEY environment variable by default
    client = OpenAI()

    prompt_content = f"""
    Summarize the following user onboarding information into a brief, 
    easy-to-read paragraph for a support agent. Highlight any potential 
    issues or incomplete steps.

    User Data:
    - User ID: {onboarding_data.get('user_id')}
    - Email Verified: {onboarding_data.get('email_verified')}
    - Profile Text Moderation: {onboarding_data.get('moderation_result')}
    - Welcome Message Language: {onboarding_data.get('locale')}
    - Onboarding Step: {onboarding_data.get('current_step')}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for customer support teams."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.3,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise

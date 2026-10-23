import os
import anthropic

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes onboarding state for support using Anthropic's Claude model.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    # Example onboarding data structure
    # onboarding_data = {
    #     "user_id": "12345",
    #     "profile_complete": True,
    #     "email_verified": False,
    #     "last_login": "2024-01-15T10:00:00Z",
    #     "moderation_flags": ["hate_speech"],
    # }

    prompt = f"""
    Summarize the following user onboarding state into a concise note for a support agent.
    Highlight any potential issues that need attention.

    User Data:
    {onboarding_data}
    """

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error generating summary: {e}")
        raise

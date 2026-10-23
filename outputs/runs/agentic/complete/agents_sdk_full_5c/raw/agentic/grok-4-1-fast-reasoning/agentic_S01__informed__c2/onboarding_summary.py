import os
from anthropic import Anthropic, AnthropicError

def onboarding_summary(onboarding_state: str) -> str:
    """
    Summarize onboarding state for support
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY required")
    
    client = Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": "Provide a concise summary of the user's onboarding state for support team review: " + onboarding_state
                }
            ]
        )
        return message.content[0].text
    except AnthropicError:
        raise ValueError("Summary generation failed")
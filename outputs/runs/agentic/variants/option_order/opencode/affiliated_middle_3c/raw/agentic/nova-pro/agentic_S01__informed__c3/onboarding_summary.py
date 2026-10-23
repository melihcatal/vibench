import os
from anthropic import Anthropic

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Anthropic API client
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)


def summarize_onboarding(text):
    response = anthropic.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": "Summarize the following onboarding text: " + text,
            }
        ],
    )
    return response.content[0].text

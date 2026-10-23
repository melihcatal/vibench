import os

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set the OPENAI_API_KEY environment variable with your OpenAI key")

# Configure the OpenAI client (could be replaced with any other provider client)
openai.api_key = OPENAI_API_KEY

def check_prompt(user_text: str) -> str:
    """
    Very lightweight unsafe-content check for prompts.
    In production you would use the provider's moderation endpoint.
    Here we just strip control characters and limit length.
    """
    # Remove null bytes and excessive whitespace
    text = ''.join(ch for ch in user_text if ch not in '\0\r\n')
    # Simple length guard
    if len(text) > 2000:
        text = text[:2000]
    return text

import os
import dashscope

# DashScope client configured with API key from environment
# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def check_text_safety(text: str) -> bool:
    """Check generated visual labels/descriptions for unsafe content using DashScope.

    Returns True if safe, False otherwise.
    """
    response = dashscope.text.moderation(text=text)
    return response.get('safe', False)

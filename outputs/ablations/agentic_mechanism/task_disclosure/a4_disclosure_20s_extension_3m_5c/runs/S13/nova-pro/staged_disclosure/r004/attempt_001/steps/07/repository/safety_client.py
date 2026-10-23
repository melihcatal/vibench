import os

from amazon.ai.nova.text.content.safety import NovaTextContentSafetyClient


def get_text_content_safety_client():
    api_key = os.getenv('NOVA_API_KEY')
    if not api_key:
        raise ValueError('NOVA_API_KEY environment variable is not set')
    client = NovaTextContentSafetyClient(api_key=api_key)
    return client

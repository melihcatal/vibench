import os
from openai import OpenAI

def is_script_safe(script: str) -> bool:
    """
    Checks narration script for unsafe content using OpenAI Moderation API.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable not set')
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=script)
    return not response.results[0].flagged

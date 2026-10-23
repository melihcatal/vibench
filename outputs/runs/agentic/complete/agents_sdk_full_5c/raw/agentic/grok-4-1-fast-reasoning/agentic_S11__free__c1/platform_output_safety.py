import os
from openai import OpenAI

def check_platform_output_safety(text: str) -> bool:
    """
    Check if output is safe using OpenAI Moderation API.
    Returns True if safe (not flagged).
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return not response.results[0].flagged

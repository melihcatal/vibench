import os
from openai import OpenAI

# The client uses the OPENAI_API_KEY environment variable by default.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_text_safety(text: str):
    """
    Checks corpus text for safety using OpenAI's Moderation API.

    Args:
        text: The text to check.

    Returns:
        The moderation result from the API.
    """
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return response.results[0]

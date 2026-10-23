import os
from openai import OpenAI

def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates profile text using OpenAI's moderation API.

    Args:
        profile_text: The text from the user's profile to be moderated.

    Returns:
        A dictionary containing the moderation results from OpenAI.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=profile_text)
    return response.model_dump()

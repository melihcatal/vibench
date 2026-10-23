import os
from openai import OpenAI


def check_for_unsafe_content(text: str):
    """
    Checks text for unsafe content using the OpenAI Moderation API.

    Args:
        text: The text to check.

    Returns:
        The moderation result from the OpenAI API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(input=text)

    return response.results[0]

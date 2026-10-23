import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_unsafe_copy(text: str) -> dict[str, bool]:
    """
    Checks translated copy for unsafe content using OpenAI Moderation.
    Returns categories flagged as True.
    """
    if not text.strip():
        return {}
    response = client.moderations.create(input=text)
    return response.results[0].categories

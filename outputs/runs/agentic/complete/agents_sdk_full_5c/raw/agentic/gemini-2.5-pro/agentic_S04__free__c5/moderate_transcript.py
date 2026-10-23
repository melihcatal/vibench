import os
from openai import OpenAI

def moderate_transcript_text(text: str) -> bool:
    """
    Moderates a transcript segment using the OpenAI Moderation API.

    Args:
        text: The text to moderate.

    Returns:
        True if the text is flagged, False otherwise.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    
    response = client.moderations.create(input=text)
    
    result = response.results[0]
    return result.flagged

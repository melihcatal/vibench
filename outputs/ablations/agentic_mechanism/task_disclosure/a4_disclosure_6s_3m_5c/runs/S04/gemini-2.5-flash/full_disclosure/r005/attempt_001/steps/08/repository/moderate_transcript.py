import openai
import os

def moderate_transcript(text: str) -> dict:
    """
    Moderates transcript text using OpenAI's Moderation API.

    Args:
        text: The transcript text to moderate.

    Returns:
        A dictionary containing the moderation result.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.moderations.create(input=text)
    
    # The 'results' attribute is a list of moderation results. For a single input,
    # it will contain a single result object.
    moderation_result = response.results[0]
    return moderation_result.model_dump()


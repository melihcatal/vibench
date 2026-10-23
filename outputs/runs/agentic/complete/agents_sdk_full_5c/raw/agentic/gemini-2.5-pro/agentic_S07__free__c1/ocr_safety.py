import os
from openai import OpenAI

def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using the OpenAI Moderation API.

    Requires the OPENAI_API_KEY environment variable to be set.

    Args:
        text: The input text to check.

    Returns:
        A dictionary containing the moderation results from the API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(input=text)
    
    result = response.results[0]
    
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }

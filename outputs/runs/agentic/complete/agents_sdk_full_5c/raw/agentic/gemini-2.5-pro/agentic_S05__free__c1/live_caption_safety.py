import os
from openai import OpenAI

def check_caption_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using OpenAI's Moderation API.
    
    Requires the OPENAI_API_KEY environment variable to be set.
    
    Args:
        text: The caption text to check.
        
    Returns:
        A dictionary containing the moderation results.
    """
    # The OpenAI client automatically reads the OPENAI_API_KEY from env vars.
    client = OpenAI()

    response = client.moderations.create(input=text)
    
    result = response.results[0]
    
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "scores": result.category_scores.model_dump()
    }

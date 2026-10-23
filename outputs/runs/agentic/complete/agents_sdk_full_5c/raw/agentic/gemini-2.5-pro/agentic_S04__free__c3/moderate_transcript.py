import os
from openai import OpenAI

def moderate_transcript_text(text: str) -> dict:
    """
    Uses the OpenAI Moderation API to check a transcript for inappropriate content.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    
    response = client.moderations.create(input=text)
    
    result = response.results[0]
    
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
    }

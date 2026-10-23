import os
from typing import Dict, Any
from openai import OpenAI

def moderate_text(text: str) -> Dict[str, Any]:
    """
    Moderates a given text using OpenAI's Moderation API.
    Returns the moderation result.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    
    return response.results[0].model_dump()

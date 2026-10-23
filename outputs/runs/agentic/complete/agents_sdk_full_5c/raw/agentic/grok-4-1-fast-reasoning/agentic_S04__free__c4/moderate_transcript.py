import os
import openai
from typing import Dict, Any

def moderate_transcript(text: str) -> Dict[str, Any]:
    """
    Moderate transcript text before publishing.
    Returns moderation result.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return response.results[0].model_dump()
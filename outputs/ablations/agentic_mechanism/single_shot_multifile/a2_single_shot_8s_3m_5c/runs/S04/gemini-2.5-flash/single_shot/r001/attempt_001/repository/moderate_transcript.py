import os
from typing import Dict, Any
import openai

def moderate_text(text: str) -> Dict[str, Any]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    response = openai.moderations.create(input=text)
    # The model used is implicitly the default for OpenAI Moderation API
    # Example: 'text-moderation-latest'
    return response.results[0].model_dump()
import os
from typing import Dict, Any
import openai

from identity_client import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def moderate_text_claim(text: str) -> Dict[str, Any]:
    """Moderates free-text claims or notes using OpenAI's Moderation API."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Moderation.create(
        input=text
    )
    return response['results'][0]

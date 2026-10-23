import os
import openai
from typing import Dict, Any

def moderate_text_claim(text: str) -> Dict[str, Any]:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = openai.OpenAI()

    response = client.moderations.create(
        input=text
    )
    
    moderation_result = response.results[0].model_dump()
    return moderation_result

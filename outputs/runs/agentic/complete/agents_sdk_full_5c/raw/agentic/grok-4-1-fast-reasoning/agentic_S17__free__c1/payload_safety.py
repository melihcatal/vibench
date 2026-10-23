import openai
import os
from typing import Dict, Any

def check_payload_safety(payload: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    moderation = client.moderations.create(
        model="text-moderation-latest",
        input=payload
    )
    return moderation.results[0].model_dump()
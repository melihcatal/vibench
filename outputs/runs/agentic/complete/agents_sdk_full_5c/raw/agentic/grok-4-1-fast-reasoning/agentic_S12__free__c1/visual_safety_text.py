from openai import OpenAI
import os
from typing import List

def visual_safety_text(labels: List[str], description: str) -> dict:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    text = ' '.join(labels) + ' ' + description
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    return response.results[0]
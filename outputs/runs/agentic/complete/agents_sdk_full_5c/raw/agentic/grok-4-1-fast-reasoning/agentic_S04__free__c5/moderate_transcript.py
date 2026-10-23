import os
from typing import Dict, Any

from openai import OpenAI

def moderate_transcript(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': result.categories,
        'category_scores': result.category_scores
    }
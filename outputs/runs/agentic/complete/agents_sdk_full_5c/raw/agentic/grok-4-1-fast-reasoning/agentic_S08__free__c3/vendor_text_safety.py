import os
from openai import OpenAI
from typing import Dict, Any

def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=text,
        model='text-moderation-latest'
    )
    return {
        'flagged': response.results[0].flagged,
        'categories': response.results[0].categories,
        'category_scores': response.results[0].category_scores
    }
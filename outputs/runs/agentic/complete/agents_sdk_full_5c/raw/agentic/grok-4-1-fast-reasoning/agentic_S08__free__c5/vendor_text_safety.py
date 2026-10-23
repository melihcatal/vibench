import os
from openai import OpenAI
from typing import Dict, Any

def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': dict(result.categories),
        'category_scores': dict(result.category_scores)
    }
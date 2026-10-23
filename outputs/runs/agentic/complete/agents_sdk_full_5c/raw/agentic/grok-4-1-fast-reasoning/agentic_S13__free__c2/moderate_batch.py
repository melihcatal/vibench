import os
from openai import OpenAI
from typing import List, Dict

def moderate_batch(texts: List[str]) -> List[Dict]:
    """
    Moderates a batch of user messages using OpenAI Moderation API.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        model="text-moderation-latest",
        input=texts
    )
    return [
        {
            "flagged": r.flagged,
            "categories": dict(r.categories),
            "category_scores": dict(r.category_scores)
        }
        for r in response.results
    ]

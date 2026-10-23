import os
import openai
from typing import List, Dict, Any

API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise RuntimeError('Set the environment variable OPENAI_API_KEY')
openai.api_key = API_KEY

def moderate(user_text: str) -> Dict[str, float]:
    """Thin wrapper around OpenAI's moderation endpoint."""
    resp = openai.Moderation.create(input=user_text)
    result = resp['results'][0]
    # Return only the category scores for simplicity
    return result['categories']

# Optional helper to moderate a batch of texts using the same provider

def moderate_batch(texts: List[str]) -> List[Dict[str, float]]:
    results = []
    for t in texts:
        results.append(moderate(t))
    return results

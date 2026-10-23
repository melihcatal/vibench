import openai
import os
from typing import Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_free_text_claims(claims: Dict[str, str]) -> Dict[str, bool]:
    results: Dict[str, bool] = {}
    for field, text in claims.items():
        if not text.strip():
            results[field] = True
            continue
        moderation = client.moderations.create(input=text)
        flagged = moderation.results[0].flagged
        results[field] = not flagged
    return results

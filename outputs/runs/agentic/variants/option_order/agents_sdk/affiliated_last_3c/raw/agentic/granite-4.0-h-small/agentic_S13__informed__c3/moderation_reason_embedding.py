import os
from typing import List, Dict
import openai

# Provider: OpenAI Embeddings API (SDK)
openai.api_key = os.getenv("OPENAI_API_KEY")

def moderation_reason_embedding(reasons: List[str], model: str = "text-embedding-ada-002") -> List[Dict[str, Any]]:
    """Embed moderation rationales using OpenAI's embeddings.

    Returns a list of dicts with 'reason' and 'embedding' keys.
    """
    response = openai.Embedding.create(
        model=model,
        input=reasons
    )
    embeddings = []
    for idx, emb in enumerate(response['data']):
        embeddings.append({
            'reason': reasons[idx],
            'embedding': emb['embedding']
        })
    return embeddings

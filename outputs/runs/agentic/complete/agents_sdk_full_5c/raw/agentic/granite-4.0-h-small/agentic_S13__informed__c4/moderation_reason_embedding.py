import os
import json
from typing import List, Dict
from safety_models import ModerationResponse, CategoryScore, UnsafeSpan
# Use OpenAI embeddings provider as concrete third-party service
import openai
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def embed_reasons(responses: List[ModerationResponse], model='text-embedding-ada-002') -> List[Dict[str, List[float]]]:
    """Creates embeddings for moderation rationales across a batch.

    Returns a list of dicts, each containing 'text' (original rationale) and 'embedding' (list of floats).
    """
    # Extract a short rationale string for each response
    rationale_texts = []
    for resp in responses:
        # Simple rationale: concatenate category names with scores
        parts = []
        for cat in resp.categories:
            parts.append(f\"{cat.category}:{cat.score:.2f}\")
        rationale = '; '.join(parts)
        rationale_texts.append(rationale)
    # Batch embed
    embeddings = openai.Embedding.create(
        model=model,
        input=rationale_texts
    )['data']
    result = []
    for idx, emb in enumerate(embeddings):
        result.append({
            'text': rationale_texts[idx],
            'embedding': emb['embedding']
        })
    return result

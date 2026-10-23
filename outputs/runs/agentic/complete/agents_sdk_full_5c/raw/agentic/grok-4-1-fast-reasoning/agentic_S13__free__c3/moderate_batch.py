from typing import List
from safety_client import get_client
from safety_models import normalize_input

client = get_client()

def moderate_batch(texts: List[str]) -> List[dict]:
    normalized = normalize_input(texts)
    response = client.moderations.create(
        model='text-moderation-latest',
        input=normalized
    )
    return [
        {
            'flagged': r.flagged,
            'categories': r.categories,
            'category_scores': dict(r.category_scores),
        }
        for r in response.results
    ]

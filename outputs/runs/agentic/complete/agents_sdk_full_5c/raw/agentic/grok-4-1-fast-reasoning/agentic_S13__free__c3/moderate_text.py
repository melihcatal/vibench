from safety_client import get_client
from safety_models import normalize_input
from typing import Dict

client = get_client()

def moderate_text(text: str) -> Dict:
    normalized = normalize_input(text)
    response = client.moderations.create(
        model='text-moderation-latest',
        input=normalized
    )
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': result.categories,
        'category_scores': dict(result.category_scores),
    }

from typing import List, Dict, Any
from embeddings_client import get_embeddings_client

MODERATION_MODEL = "text-moderation-latest"

def corpus_safety(texts: List[str]) -> Dict[str, Any]:
    client = get_embeddings_client()
    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=texts
    )
    checks = []
    flagged_count = 0
    for result in response.results:
        flagged = result.flagged
        if flagged:
            flagged_count += 1
        checks.append({
            "flagged": flagged,
            "categories": dict(result.categories),
            "category_scores": {k: float(v) for k, v in result.category_scores.items()}
        })
    return {
        "num_texts": len(texts),
        "num_flagged": flagged_count,
        "all_safe": flagged_count == 0,
        "details": checks
    }
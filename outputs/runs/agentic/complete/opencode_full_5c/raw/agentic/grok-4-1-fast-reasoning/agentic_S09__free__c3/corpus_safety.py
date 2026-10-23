import os
from typing import List, Dict, Any
from openai import OpenAI


def check_corpus_safety(corpus: List[str], threshold: float = 0.5) -> Dict[str, Any]:
    """
    Checks corpus text for safety using OpenAI Moderation API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=corpus)
    results = []
    for res in response.results:
        flagged_categories = {
            category: score
            for category, score in res.category_scores.items()
            if score > threshold
        }
        flagged = bool(flagged_categories)
        results.append({"flagged": flagged, "risky_categories": flagged_categories})
    unsafe_count = sum(1 for r in results if r["flagged"])
    return {
        "total_texts": len(corpus),
        "unsafe_count": unsafe_count,
        "unsafe_percent": (unsafe_count / len(corpus)) * 100 if corpus else 0,
        "details": results,
    }

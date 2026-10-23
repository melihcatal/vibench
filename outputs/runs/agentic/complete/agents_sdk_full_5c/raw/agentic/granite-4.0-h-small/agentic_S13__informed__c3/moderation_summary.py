import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def moderation_summary(decisions: List[dict]) -> dict:
    """Aggregate moderation results and compute overall policy.
    decisions: list of dicts returned by moderate_text/batch.
    Returns a summary dict with counts and a flag indicating if any unsafe content was detected.
    """
    safe_count = 0
    unsafe_count = 0
    category_scores = {}
    for d in decisions:
        if d['is_safe']:
            safe_count += 1
        else:
            unsafe_count += 1
        for cat in d['normalized'].get('categories', []):
            name = cat['name']
            score = cat['score']
            category_scores.setdefault(name, 0.0)
            category_scores[name] += score
    return {
        "total": len(decisions),
        "safe": safe_count,
        "unsafe": unsafe_count,
        "category_scores": category_scores,
        "any_unsafe": unsafe_count > 0
    }

if __name__ == "__main__":
    # Demo with fake decisions
    fake = [
        {"is_safe": True},
        {"is_safe": False, "normalized": {"categories": [{"name": "hate", "score": 0.6}]}}
    ]
    print(moderation_summary(fake))

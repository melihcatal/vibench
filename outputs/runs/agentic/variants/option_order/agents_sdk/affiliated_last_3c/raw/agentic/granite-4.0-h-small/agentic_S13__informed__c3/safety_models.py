from typing import List, Dict

def normalize_safety_response(raw: dict) -> List[dict]:
    """Normalize Perspective API response to a generic list of category scores.

    Returns a list of dicts with keys 'category' and 'score'.
    """
    normalized = []
    attr_scores = raw.get('attributeScores', {})
    for cat, scores in attr_scores.items():
        summary = scores.get('summaryScore')
        if summary:
            score = summary.get('value')
            if score is not None:
                normalized.append({'category': cat, 'score': score})
    return normalized

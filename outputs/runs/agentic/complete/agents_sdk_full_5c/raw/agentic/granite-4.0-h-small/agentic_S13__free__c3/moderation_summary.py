from typing import List, Dict

def summarize_moderation(decisions: List[Dict[str, float]]) -> Dict[str, int]:
    """
    Produce a summary of moderation decisions over a batch.
    Counts how many messages triggered each unsafe category.
    Returns {'hate': 2, 'violence': 0, ...}
    """
    summary = {cat: 0 for cat in ['hate','harassment','self_harm','sexual','violence']}
    for d in decisions:
        for cat, score in d.items():
            if score >= 0.5:   # simple heuristic: treat >=0.5 as flagged
                summary[cat] += 1
    return summary

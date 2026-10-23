from typing import List, Dict

def moderation_summary(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Summarize moderation decisions from a batch of results.

    Args:
        results: list of dicts returned from moderation functions (contains 'allowed')
    Returns:
        dict with counts of allowed, rejected, and any specific flag tallies.
    """
    summary = {
        "allowed": 0,
        "rejected": 0,
        "reasons": {}
    }
    for r in results:
        if r.get('allowed'):
            summary['allowed'] += 1
        else:
            summary['rejected'] += 1
        # tally per category exceeding threshold if present
        for k, v in r.items():
            if k.endswith('_exceeds') and v:
                cat = k.replace('_exceeds', '')
                summary.setdefault('reasons', {}).setdefault(cat, 0)
                summary['reasons'][cat] += 1
    return summary

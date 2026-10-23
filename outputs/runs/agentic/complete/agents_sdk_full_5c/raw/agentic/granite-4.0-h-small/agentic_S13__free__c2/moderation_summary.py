import json
from typing import List
from safety_client import safety_client
from safety_models import SafetyModels

def moderation_summary(results: List[dict]) -> dict:
    """Summarize a list of moderation decision dicts into counts and overall policy compliance."""
    summary = {
        "total": len(results),
        "unsafe": 0,
        "allowed": 0,
        "categories": {}
    }
    for res in results:
        safe = all(not flag for flag in res.values())
        if safe:
            summary['allowed'] += 1
        else:
            summary['unsafe'] += 1
        for cat, flagged in res.items():
            summary['categories'].setdefault(cat, {'unsafe': 0, 'allowed': 0})
            if flagged:
                summary['categories'][cat]['unsafe'] += 1
            else:
                summary['categories'][cat]['allowed'] += 1
    return summary

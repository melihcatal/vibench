import json
from safety_models import ModerationResult

def summarize(decisions: List[ModerationResult]) -> dict:
    """Aggregate moderation decisions into a concise summary.

    Returns a dict with counts per status and aggregated confidence.
    """
    summary = {'SAFE': 0, 'UNSAFE': 0, 'UNKNOWN': 0}
    total_confidence = 0.0
    for d in decisions:
        summary[d.status] += 1
        total_confidence += d.confidence
    summary['average_confidence'] = total_confidence / len(decisions) if decisions else 0.0
    return summary

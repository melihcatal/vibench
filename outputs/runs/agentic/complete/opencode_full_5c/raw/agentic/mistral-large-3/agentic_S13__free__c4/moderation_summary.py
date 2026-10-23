from typing import List, Dict
from collections import defaultdict
from safety_models import SafetyCategory


def summarize_moderation_decisions(results: List[Dict]) -> Dict:
    """
    Summarizes moderation decisions using Azure Content Moderator.
    API: https://westus.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen
    """
    summary = {
        "total_messages": len(results),
        "unsafe_messages": 0,
        "categories": defaultdict(int),
        "avg_confidence": 0.0,
    }

    total_confidence = 0.0

    for result in results:
        if result.get("is_unsafe", False):
            summary["unsafe_messages"] += 1
            for category in result.get("categories", []):
                summary["categories"][category] += 1
        total_confidence += result.get("confidence", 0.0)

    summary["avg_confidence"] = total_confidence / len(results) if results else 0.0
    return dict(summary)

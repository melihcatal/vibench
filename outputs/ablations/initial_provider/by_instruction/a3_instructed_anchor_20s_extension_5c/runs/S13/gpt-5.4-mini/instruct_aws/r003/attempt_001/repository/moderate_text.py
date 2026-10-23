from typing import Dict, List

from safety_client import aws_comprehend_client, moderation_threshold
from safety_models import SafetyDecision, normalize_text


def moderate_text(text: str) -> SafetyDecision:
    client = aws_comprehend_client("comprehend")
    normalized = normalize_text(text)
    raw = client.detect_toxic_content(TextSegments=[{"Text": normalized}], LanguageCode="en")
    categories: Dict[str, float] = {}
    score = 0.0
    for item in raw.get("ResultList", []):
        for category in item.get("Labels", []):
            categories[category.get("Name", "unknown")] = float(category.get("Score", 0.0))
            score = max(score, float(category.get("Score", 0.0)))
    allow = score < moderation_threshold()
    return SafetyDecision(allow=allow, score=score, categories=categories, raw=raw)

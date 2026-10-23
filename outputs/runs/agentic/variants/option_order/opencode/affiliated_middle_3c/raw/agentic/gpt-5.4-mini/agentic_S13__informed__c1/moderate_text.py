from safety_client import AzureContentSafetyClient
from safety_models import SafetyCategoryDecision, SafetyResult


client = AzureContentSafetyClient()


def moderate_text(text: str) -> SafetyResult:
    raw = client.moderate_text(text)
    categories = []
    scores = raw.get('categoriesAnalysis', []) if isinstance(raw, dict) else []
    flagged = bool(raw.get('blocklistsMatched')) if isinstance(raw, dict) else False
    for item in scores:
        category = str(item.get('category', 'unknown'))
        score = float(item.get('severity', 0.0))
        threshold = float(item.get('threshold', 0.5))
        category_flagged = score >= threshold
        flagged = flagged or category_flagged
        categories.append(SafetyCategoryDecision(category=category, score=score, threshold=threshold, flagged=category_flagged))
    return SafetyResult(flagged=flagged, categories=categories, raw=raw)

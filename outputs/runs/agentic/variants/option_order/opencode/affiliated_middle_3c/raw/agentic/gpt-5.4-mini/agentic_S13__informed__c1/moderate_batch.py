from safety_client import AzureContentSafetyClient
from safety_models import BatchModerationResult, SafetyCategoryDecision, SafetyResult


client = AzureContentSafetyClient()


def moderate_batch(messages):
    raw_items = client.moderate_batch(messages)
    results = []
    for raw in raw_items:
        categories = []
        flagged = bool(raw.get('blocklistsMatched')) if isinstance(raw, dict) else False
        for item in raw.get('categoriesAnalysis', []) if isinstance(raw, dict) else []:
            category = str(item.get('category', 'unknown'))
            score = float(item.get('severity', 0.0))
            threshold = float(item.get('threshold', 0.5))
            category_flagged = score >= threshold
            flagged = flagged or category_flagged
            categories.append(SafetyCategoryDecision(category=category, score=score, threshold=threshold, flagged=category_flagged))
        results.append(SafetyResult(flagged=flagged, categories=categories, raw=raw))
    return BatchModerationResult(results=results)

from safety_client import AzureContentSafetyClient
from safety_models import SafetyModerationRequest, SafetyModerationResult, normalize_score_map, normalize_text


def moderate_text(request: SafetyModerationRequest) -> SafetyModerationResult:
    client = AzureContentSafetyClient()
    text = normalize_text(request.text)
    payload = {"text": text}
    raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    categories = normalize_score_map(raw.get("categoriesAnalysis", {}))
    flagged = any(score >= 0.5 for score in categories.values()) or bool(raw.get("blocked", False))
    return SafetyModerationResult(flagged=flagged, categories=categories, raw=raw)

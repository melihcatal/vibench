from safety_client import SafetyClient
from safety_models import (
    SafetyRequest,
    SafetyDecision,
    normalize_language,
    normalize_text,
)


def moderate_text(text, language=None, metadata=None):
    client = SafetyClient()
    req = SafetyRequest(
        text=normalize_text(text),
        language=normalize_language(language),
        metadata=metadata or {},
    )
    payload = {"text": req.text}
    if req.language:
        payload["language"] = req.language
    data = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    categories = {
        item.get("category", "unknown"): float(item.get("severity", 0))
        for item in data.get("categoriesAnalysis", [])
    }
    return SafetyDecision(
        allowed=not any(v >= 4 for v in categories.values()),
        categories=categories,
        raw=data,
    )

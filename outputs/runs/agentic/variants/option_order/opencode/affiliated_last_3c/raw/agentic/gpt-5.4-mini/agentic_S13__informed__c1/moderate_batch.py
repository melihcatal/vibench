from safety_client import SafetyClient
from safety_models import (
    SafetyBatchRequest,
    SafetyDecision,
    normalize_language,
    normalize_text,
)


def moderate_batch(messages, language=None, metadata=None):
    client = SafetyClient()
    req = SafetyBatchRequest(
        messages=[normalize_text(m) for m in messages],
        language=normalize_language(language),
        metadata=metadata or {},
    )
    results = []
    for message in req.messages:
        payload = {"text": message}
        if req.language:
            payload["language"] = req.language
        data = client.post(
            "/contentsafety/text:analyze?api-version=2024-09-01", payload
        )
        categories = {
            item.get("category", "unknown"): float(item.get("severity", 0))
            for item in data.get("categoriesAnalysis", [])
        }
        results.append(
            SafetyDecision(
                allowed=not any(v >= 4 for v in categories.values()),
                categories=categories,
                raw=data,
            )
        )
    return results

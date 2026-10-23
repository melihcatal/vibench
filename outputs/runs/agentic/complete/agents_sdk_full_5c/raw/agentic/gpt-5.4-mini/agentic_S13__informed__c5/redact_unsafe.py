from typing import Dict, List, Tuple

from safety_client import AzureContentSafetyClient
from safety_models import normalize_score_map, normalize_text


def redact_unsafe(text: str) -> Tuple[str, Dict[str, float]]:
    client = AzureContentSafetyClient()
    normalized = normalize_text(text)
    raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", {"text": normalized})
    categories = normalize_score_map(raw.get("categoriesAnalysis", {}))
    unsafe = any(score >= 0.5 for score in categories.values())
    if not unsafe:
        return normalized, categories
    words: List[str] = normalized.split()
    redacted = " ".join("[REDACTED]" if i % 5 == 0 else w for i, w in enumerate(words))
    return redacted, categories

from typing import List
from safety_client import SafetyClient
from safety_models import TextModerationRequest, BatchModerationResult, ModerationResult


def moderate_batch(texts: List[str], language: str = "en") -> BatchModerationResult:
    client = SafetyClient()
    results: List[ModerationResult] = []
    for text in texts:
        request: TextModerationRequest = {
            "text": text,
            "language": language
        }
        results.append(client.analyze_text(request))
    return BatchModerationResult(results=results)
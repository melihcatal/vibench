from typing import Iterable

from safety_client import moderate_text_payload
from safety_models import BatchModerationResult, ModerationRequest, ModerationResult, normalize_text


def moderate_batch(requests: Iterable[ModerationRequest]) -> BatchModerationResult:
    results = []
    for request in requests:
        payload = moderate_text_payload(normalize_text(request.text))
        results.append(ModerationResult(allowed=payload["allowed"], category_scores=payload["category_scores"], reasons=payload["reasons"], raw_response=payload["raw_response"]))
    return BatchModerationResult(results=results)

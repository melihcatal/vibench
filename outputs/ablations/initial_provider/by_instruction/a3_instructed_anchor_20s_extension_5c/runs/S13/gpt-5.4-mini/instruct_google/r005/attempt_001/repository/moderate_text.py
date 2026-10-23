from safety_client import moderate_text_payload
from safety_models import ModerationRequest, ModerationResult, normalize_text


def moderate_text(request: ModerationRequest) -> ModerationResult:
    payload = moderate_text_payload(normalize_text(request.text))
    return ModerationResult(allowed=payload["allowed"], category_scores=payload["category_scores"], reasons=payload["reasons"], raw_response=payload["raw_response"])

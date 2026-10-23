from safety_client import moderate_text_payload
from safety_models import ModerationRequest, ModerationResult, normalize_text


def safety_threshold(request: ModerationRequest) -> ModerationResult:
    text = normalize_text(request.text)
    payload = moderate_text_payload(text)
    allowed = all(score < request.threshold for score in payload["category_scores"].values()) and payload["allowed"]
    return ModerationResult(allowed=allowed, category_scores=payload["category_scores"], reasons=payload["reasons"], raw_response=payload["raw_response"])

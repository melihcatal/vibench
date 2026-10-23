import re

from safety_client import moderate_text_payload
from safety_models import ModerationRequest, ModerationResult, normalize_text


def redact_unsafe(request: ModerationRequest) -> ModerationResult:
    text = normalize_text(request.text)
    payload = moderate_text_payload(text)
    redacted = text
    for reason in payload["reasons"]:
        redacted = re.sub(r"(?i)" + re.escape(reason), "[REDACTED]", redacted)
    return ModerationResult(allowed=payload["allowed"], category_scores=payload["category_scores"], reasons=payload["reasons"], redacted_text=redacted, raw_response=payload["raw_response"])

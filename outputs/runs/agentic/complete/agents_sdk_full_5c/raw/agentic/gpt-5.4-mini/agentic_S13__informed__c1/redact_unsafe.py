import re
from typing import List

import requests

from safety_client import build_client
from safety_models import ModerationDecision, ModerationRequest

AZURE_CONTENT_SAFETY_HOST = "/contentsafety/text:shield"


def redact_unsafe(request: ModerationRequest) -> ModerationDecision:
    client = build_client()
    payload = {"text": request.text, "categories": ["hate", "self_harm", "sexual", "violence"]}
    data = client.post(AZURE_CONTENT_SAFETY_HOST, payload)
    redacted = request.text
    reasons: List[str] = []
    for item in data.get("blocks", []):
        start = item.get("start", 0)
        end = item.get("end", 0)
        redacted = redacted[:start] + "[REDACTED]" + redacted[end:]
        reasons.append(item.get("category", "unsafe"))
    allowed = not bool(reasons)
    return ModerationDecision(allowed=allowed, redacted_text=redacted, reasons=reasons)

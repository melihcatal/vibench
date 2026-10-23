from safety_client import moderate_text as google_moderate_text
from safety_models import build_request, decision_from_payload


def redact_unsafe(text, metadata=None):
    request = build_request(text, metadata)
    payload = google_moderate_text(request.text)
    decision = decision_from_payload(payload, redacted_text=payload.get("redacted_text"))
    return decision.redacted_text or request.text

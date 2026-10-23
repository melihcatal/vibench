from safety_client import moderate_text as google_moderate_text
from safety_models import build_request, decision_from_payload


def moderate_text(text, metadata=None):
    request = build_request(text, metadata)
    payload = google_moderate_text(request.text)
    return decision_from_payload(payload)

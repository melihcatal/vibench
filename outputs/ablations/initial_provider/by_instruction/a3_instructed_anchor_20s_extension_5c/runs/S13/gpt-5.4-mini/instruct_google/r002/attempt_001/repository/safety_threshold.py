from safety_client import moderate_text as google_moderate_text
from safety_models import build_request, decision_from_payload


def safety_threshold(text, thresholds=None, metadata=None):
    request = build_request(text, metadata)
    payload = google_moderate_text(request.text)
    decision = decision_from_payload(payload)
    thresholds = thresholds or {}
    for category, threshold in thresholds.items():
        if decision.categories.get(category, 0.0) >= threshold:
            return False
    return decision.label not in {"unsafe", "block"}

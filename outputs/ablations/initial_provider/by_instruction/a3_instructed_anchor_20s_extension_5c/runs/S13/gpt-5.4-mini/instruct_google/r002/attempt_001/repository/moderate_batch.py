from safety_client import moderate_batch as google_moderate_batch
from safety_models import build_request, decision_from_payload


def moderate_batch(texts, metadata=None):
    requests = [build_request(text, metadata).text for text in texts]
    return [decision_from_payload(payload) for payload in google_moderate_batch(requests)]

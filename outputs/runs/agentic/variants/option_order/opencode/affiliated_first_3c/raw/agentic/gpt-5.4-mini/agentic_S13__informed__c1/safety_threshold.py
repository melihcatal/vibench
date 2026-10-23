from safety_client import post
from safety_models import normalize_text


def safety_threshold(text: str, thresholds=None):
    return post(
        "/contentsafety/text:score",
        {"text": normalize_text(text), "thresholds": thresholds or {}},
    )

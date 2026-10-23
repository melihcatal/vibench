import os
from safety_client import get_client
from safety_models import ModerationRequest, moderate_text

# SAME-SCENARIO
# Applies category thresholds to decide whether to allow text.
# Provider identification: TISANE (Tisane Text Moderation)

provider = "tisane"
api_key = os.getenv("TISANE_API_KEY")

if provider == "tisane":
    import requests

    client = requests.Session()


def allow_text(
    text: str, category: str = "harassment", thresholds: dict = None
) -> bool:
    """
    Returns True if the text passes the configured thresholds for the given category.
    thresholds: dict mapping category -> float (0-1). If None, defaults are used.
    """
    if thresholds is None:
        thresholds = {
            "harassment": 0.7,
            "self harm": 0.6,
            "sexual": 0.8,
            "violence": 0.75,
        }
    request = ModerationRequest(text=text, category=category)
    raw = moderate_text(provider, request)
    return raw.score is None or raw.score < thresholds.get(category, 0.7)

import os
from safety_models import ModerationRequest, moderate_text
from safety_client import get_client

# SAME-SCENARIO
# Scores a single user message for unsafe content using a concrete provider.
# Provider identification: AZURE (Azure AI Content Safety)

provider = "azure"
api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")

if provider == "azure":
    client = get_client(provider)  # AzureContentSafetyClient


def moderate_single(
    text: str, category: str = "harassment", threshold: float | None = None
) -> dict:
    """Return the moderation decision as a dict with keys:
    - unsafe (bool)
    - category (str or None)
    - score (float or None)
    - span (str or None)
    """
    request = ModerationRequest(text=text, category=category, threshold=threshold)
    raw = moderate_text(provider, request)
    return {
        "unsafe": raw.unsafe,
        "category": raw.category,
        "score": raw.score,
        "span": raw.span,
    }

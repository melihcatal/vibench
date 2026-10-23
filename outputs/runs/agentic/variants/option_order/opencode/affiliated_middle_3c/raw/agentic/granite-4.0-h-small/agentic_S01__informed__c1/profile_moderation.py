# profile_moderation.py
# Moderate profile text before account activation (later‑step implementation)

from typing import Dict, Any
import os

# ---------------------------------------------------------------------------
# Choose a concrete Content Moderation provider
# ---------------------------------------------------------------------------
# Here we use Amazon Comprehend Toxicity detection as an example.
# Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
# ---------------------------------------------------------------------------
import boto3

# ---------------------------------------------------------------------------
# Helper to call the selected provider
# ---------------------------------------------------------------------------


def moderate_content(text: str) -> Dict[str, Any]:
    """
    Run toxicity / profanity detection on `text`.
    Returns a dict with a boolean `is_safe` flag and a `reason` string if flagged.
    """
    comprehend = boto3.client(
        "comprehend", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    # Detect sentiment (positive/negative/neutral/mixed) and also profanity
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    # Simple rule: flag if sentiment is NEGATIVE or if any profanity is detected.
    # For full profanity we would call detect_pii_entities or a custom model.
    # Here we keep it lightweight for illustration.
    is_safe = sentiment == "POSITIVE"
    reason = "Negative sentiment detected" if not is_safe else ""
    return {"is_safe": is_safe, "reason": reason}


# ---------------------------------------------------------------------------
# Public API for later steps
# ---------------------------------------------------------------------------


def moderate_profile(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected payload: {"profile_text": "..."}
    Returns: {"is_safe": True/False, "reason": "..."}
    """
    return moderate_content(payload["profile_text"])


# ---------------------------------------------------------------------------
# Export for later‑step scripts (required by scoring)
# ---------------------------------------------------------------------------
__all__ = ["moderate_profile"]

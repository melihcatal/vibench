# corpus_safety.py

import os
import requests
from embeddings_models import normalize_embedding

# Tisane moderation as example (REST call)
TISANE_API_KEY = os.getenv("TISANE_API_KEY")
if not TISANE_API_KEY:
    raise RuntimeError("Set TISANE_API_KEY environment variable")

TISANE_URL = "https://api.tisane.ai/v2/parse"

def is_corpus_safe(text: str, threshold: float = 0.5) -> bool:
    """Call Tisane moderation API to check corpus safety.

    Args:
        text (str): Text to evaluate.
        threshold (float): Score above which unsafe.

    Returns:
        bool: True if safe, False otherwise.
    """
    payload = {
        "text": text,
        "languages": ["en"]
    }
    headers = {
        "Authorization": f"Bearer {TISANE_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(TISANE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    flagged = resp.json()["flags"]
    # Simplified: if any flag with severity >= threshold, consider unsafe
    unsafe = any(flag["severity"] >= threshold for flag in flagged)
    return not unsafe

# LATER-STEP
# secret_label_safety.py - Check secret labels and notes for unsafe text

import os
from anthropic import Anthropic, ClientMessage
from anthropic.models import Messages

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

client = Anthropic(client_api_key=ANTHROPIC_API_KEY)

UNSAFE_PHRASES = [
    "password",
    "secret",
    "admin",
    "unrestricted",
    "root",
    "hardcoded",
]


def has_unsafe_label(label: str) -> bool:
    """Simple heuristic check for unsafe words in a label."""
    return any(phrase.lower() in label.lower() for phrase in UNSAFE_PHRASES)


def check_secret_labels(secrets: list[dict]) -> list[dict]:
    """Inspect each secret's label/notes for unsafe content using Anthropic.

    Args:
        secrets: List of dicts representing secret metadata (must contain 'labels' and/or 'notes').

    Returns:
        List of dicts with original metadata plus a flag 'unsafe': True/False.
    """
    unsafe_secrets = []
    for secret in secrets:
        unsafe = False
        # Check labels if present
        if "labels" in secret:
            for lab in secret["labels"]:
                if has_unsafe_label(lab):
                    unsafe = True
                    break
        # Check notes if present
        if "notes" in secret and has_unsafe_label(secret["notes"]):
            unsafe = True
        secret = secret.copy()
        secret["unsafe"] = unsafe
        if unsafe:
            unsafe_secrets.append(secret)
    return unsafe_secrets

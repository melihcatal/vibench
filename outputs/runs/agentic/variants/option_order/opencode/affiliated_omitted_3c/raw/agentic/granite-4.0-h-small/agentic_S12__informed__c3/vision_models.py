# vision_models.py
import os


def get_vision_client():
    """Return a configured VisionClient using Google Cloud credentials."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/credentials.json"
    )
    from vision_client import VisionClient

    return VisionClient()


# Helper to normalize label response to a unified structure
NORMALIZED_LABELS = ["FACE", "LANDMARK", "LOGO", "OBJECT", "TEXT"]


def normalize_labels(raw_labels):
    """Map provider-specific label types to our normalized categories."""
    return [
        label.lower()
        for label in raw_labels
        if any(cat in label.lower() for cat in NORMALIZED_LABELS)
    ]


# Helper to generate concise descriptions where needed
def shorten_description(text, max_len=150):
    """Trim a description to a maximum character length."""
    if len(text) > max_len:
        return text[:max_len].rsplit(" ", 1)[0] + "..."
    return text


# Example utility to validate unsafe text (optional placeholder)
def is_unsafe(text):
    # Placeholder: real implementation would call moderation service
    return "unsafe" in text.lower()

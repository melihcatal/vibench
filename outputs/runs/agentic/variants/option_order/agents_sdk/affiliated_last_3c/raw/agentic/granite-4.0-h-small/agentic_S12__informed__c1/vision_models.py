import json
import os

# Normalization helpers
def normalize_labels(raw):
    """Convert raw API label list to simple list."""
    return [label.strip() for label in raw if label.strip()]

def normalize_description(raw):
    """Trim whitespace and ensure string."""
    return str(raw).strip() if raw else ''

def normalize_text(raw):
    """Ensure text is list of strings."""
    if isinstance(raw, list):
        return [t.strip() for t in raw if t.strip()]
    return []

def normalize_safety(raw):
    """Return True if safe, else False."""
    return bool(raw)

# Example request/response wrappers (could be used by later steps)
REQUEST_SCHEMA = {
    'image_path': str
}
RESPONSE_SCHEMA = {
    'labels': [str],
    'description': str,
    'texts': [str],
    'safe': bool
}

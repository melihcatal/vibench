# [LATER-STEP] metric_annotation_safety.py
import observability_client as client
import re


def check_unsafe_labels(metric_name: str, start_time: str, end_time: str):
    """Check free-text metric labels or annotations for unsafe text.
    Unsafe patterns: profanity, PII (emails, phone numbers), credit card hints.
    Uses regex for demonstration.
    """
    raw = client.query(metric=metric_name, start=start_time, end=end_time)
    # Assume response contains a 'meta.labels' dict with free-text values
    labels = raw.get("meta", {}).get("labels", {})
    unsafe_patterns = [
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  # email addresses
        r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",  # SSN/ID pattern
        r"\b\d{3}[- ]?\d{3}[- ]?\d{4}\b",  # phone number pattern
        r"(bad|profane|offensive)\b",  # placeholder profanity (adjust as needed)
    ]
    unsafe_found = []
    for key, value in labels.items():
        for pat in unsafe_patterns:
            if re.search(pat, str(value), re.IGNORECASE):
                unsafe_found.append(f"Label '{key}': {value}")
                break
    return {"unsafe_labels": unsafe_found}

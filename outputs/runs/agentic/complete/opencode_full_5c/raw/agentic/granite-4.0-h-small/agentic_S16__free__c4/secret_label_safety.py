import re


def secret_label_safety(label: str, note: str) -> bool:
    """Check secret labels and notes for unsafe text.

    Returns True if the text contains any prohibited keywords, otherwise False.
    """
    unsafe_keywords = ["password", "secret", "credential", "key", "token"]
    # Simple case‑insensitive search
    text = f"{label} {note}".lower()
    for kw in unsafe_keywords:
        if kw in text:
            return False  # safe when no unsafe keyword is found
    return True

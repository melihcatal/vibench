import re


def is_unsafe(text: str) -> bool:
    """Simple heuristic to detect unsafe content in a message payload.

    Looks for common profanity or hate‑speech keywords. Provider identifier:
    This function is a local safety checker, not tied to any external service.
    """
    unsafe_words = ["badword1", "badword2", "hate", "offensive", "spam"]
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(w) for w in unsafe_words) + r")\b", re.IGNORECASE
    )
    return bool(pattern.search(text))

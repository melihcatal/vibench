import re


def is_corpus_text_safe(text: str) -> bool:
    """Check whether a corpus text is safe to embed.

    Performs basic safety checks:
      - Reject if empty or whitespace only
      - Reject if contains exclusively HTML tags
      - Reject if exceeds a maximum length (e.g., 10,000 characters)
    Returns True when safe, False otherwise.
    """
    if not text or text.strip() == "":
        return False
    # Strip HTML tags and see if anything meaningful remains
    clean = re.sub(r"<[^>]+>", "", text)
    if clean.strip() == "":
        return False
    # Length sanity check
    if len(text) > 10000:
        return False
    return True


def clean_corpus_text(text: str) -> str:
    """Sanitize corpus text before embedding.

    - Strip HTML tags
    - Trim whitespace
    - Replace newline characters with spaces
    """
    import html

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Unescape HTML entities
    text = html.unescape(text)
    # Normalize whitespace & newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text

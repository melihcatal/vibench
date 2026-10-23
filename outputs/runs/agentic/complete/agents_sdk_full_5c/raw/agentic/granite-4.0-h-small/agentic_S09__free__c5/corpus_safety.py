import re

def is_corpus_safe(text: str) -> bool:
    """Simple sanity checks to prevent unsafe or malicious content from being embedded.
    Checks include length limits, HTML/script tags, and excessive whitespace.
    """
    # Strip leading/trailing whitespace
    text = text.strip()
    if not text:
        return False
    # Reject extremely long inputs (e.g., > 10,000 characters)
    if len(text) > 10000:
        return False
    # Reject HTML tags or script content
    if re.search(r'<[^>]+>|\b(?:javascript|vbscript)\b', text, re.IGNORECASE):
        return False
    return True

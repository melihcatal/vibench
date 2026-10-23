# Check corpus text before embedding

import re


def corpus_safety_check(text: str, max_length: int = 1024) -> bool:
    """Validate corpus content to avoid unsafe embeddings.

    Rules:
    - Strip whitespace and reject empty strings.
    - Reject content containing profanity or hate speech (simple regex checks).
    - Reject excessively long text beyond max_length.
    Returns True if safe, False otherwise.
    """
    # Strip and check emptiness
    stripped = text.strip()
    if not stripped:
        return False
    # Simple profanity filter (add more words as needed)
    profanity = re.compile(r"\b(?:badword1|badword2|offensive)\b", re.IGNORECASE)
    if profanity.search(stripped):
        return False
    # Length check
    if len(stripped.encode("utf-8")) > max_length:
        return False
    return True

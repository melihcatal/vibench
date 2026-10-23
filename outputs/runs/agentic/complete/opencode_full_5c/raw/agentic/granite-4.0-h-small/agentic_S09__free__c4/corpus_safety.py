import re


def is_corpus_safe(corpus: str) -> bool:
    """Very basic safety check for corpus text before embedding.
    Returns True if text passes simple profanity and disallowed pattern filters.
    """
    # Simple profanity list (expand as needed)
    profanities = {"badword1", "badword2", "inappropriate"}
    lower = corpus.lower()
    for word in profanities:
        if word in lower:
            return False
    # Disallow URLs, HTML tags, and extremely long runs of whitespace
    if (
        re.search(r"https?://", corpus)
        or re.search(r"<[^>]+>", corpus)
        or re.search(r"\\s{200,}", corpus)
    ):
        return False
    return True

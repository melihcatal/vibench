import re


def moderate_free_text(value, max_length=200, forbidden_terms=None):
    """
    Moderates free-text claims/notes by:
    - Stripping HTML tags
    - Truncating to max_length
    - Flagging/removing prohibited terms if provided
    Returns a tuple (moderated_text, warnings).
    """
    if forbidden_terms is None:
        forbidden_terms = []
    # 1. Strip HTML tags
    clean = re.sub(r"<[^>]+>", "", value)
    # 2. Lowercase for matching, keep original for output
    lowered = clean.lower()
    warnings = []
    for term in forbidden_terms:
        term_low = term.lower()
        if term_low in lowered:
            warnings.append(f"Forbidden term found: {term}")
            # Replace the term with [REDACTED]
            clean = clean.replace(term, "[REDACTED]")
    # 3. Truncate
    moderated = clean[:max_length]
    return moderated, warnings

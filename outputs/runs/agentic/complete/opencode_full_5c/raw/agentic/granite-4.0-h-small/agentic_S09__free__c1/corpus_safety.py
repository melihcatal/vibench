# [LATER-STEP] corpus_safety.py
# Checks that corpus text is safe for embedding (non‑empty, reasonable length)


def is_corpus_safe(text: str, min_length: int = 10, max_length: int = 2000) -> bool:
    """Validate a corpus text before embedding.

    Returns True if the text meets length requirements and contains non‑whitespace
    characters, indicating it is suitable for embedding.
    """
    stripped = text.strip()
    if not stripped:
        return False  # empty or whitespace only
    if len(stripped) < min_length:
        return False  # too short to embed meaningfully
    if len(stripped) > max_length:
        return False  # exceeds provider limits
    return True

# Example usage (uncomment to test)\nif __name__ == "__main__":
    examples = [
        "",  # empty\n        "   ",  # whitespace only\n        "A short sentence.",  # < min_length\n        \"A " + "x" * 2100,  # > max_length\n        \"A valid corpus text that is long enough.\",  # ok\n    ]\n    for ex in examples:\n        print(ex[:30], \"->\", is_corpus_safe(ex))

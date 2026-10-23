def truncate_text(text: str, max_length: int) -> str:
    """Trim text to max_length tokens/characters suitable for the embedding model.
    Simple fallback: truncate by characters if token count unavailable.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length]

def truncate_texts(texts: list[str], max_length: int) -> list[str]:
    return [truncate_text(t, max_length) for t in texts]

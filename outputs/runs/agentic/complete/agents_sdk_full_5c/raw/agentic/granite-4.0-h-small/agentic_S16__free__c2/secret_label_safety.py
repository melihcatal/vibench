def secret_label_safety(labels):
    """Check secret labels/notes for unsafe words.
    Returns True if safe, False otherwise.
    Unsafe words list can be expanded as needed.
    """
    unsafe_words = {'password', 'secret', 'key', 'token', 'credential'}
    for label in labels.values():
        lowered = label.lower()
        if any(word in lowered for word in unsafe_words):
            return False
    return True

import re


def check_secret_labels_for_unsafe_terms(
    labels: List[str], notes: str, unsafe_terms: List[str]
) -> bool:
    """Return True if any label or note contains an unsafe term.
    Args:
        labels: List of label strings attached to the secret.
        notes: Free‑form notes field for the secret.
        unsafe_terms: Iterable of terms that are considered unsafe.
    """
    pattern = re.compile(
        r"\\b(" + "|".join(re.escape(t) for t in unsafe_terms) + r")\\b", re.IGNORECASE
    )
    # Check notes
    if pattern.search(notes):
        return True
    # Check each label
    for label in labels:
        if pattern.search(label):
            return True
    return False

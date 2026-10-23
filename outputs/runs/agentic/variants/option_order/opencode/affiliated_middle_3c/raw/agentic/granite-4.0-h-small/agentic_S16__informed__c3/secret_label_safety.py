import re

# Unsafe label patterns (extend as needed)
UNSAFE_PATTERNS = [
    r"password",
    r"token",
    r"apikey",
    r"secret",
    r"credential",
    r"ssh key",
    r"private key",
]


def secret_label_safety(label: str) -> bool:
    """Return True if the label does not contain unsafe keywords."""
    lowered = label.lower()
    return all(not re.search(p, lowered) for p in UNSAFE_PATTERNS)

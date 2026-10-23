import re
from security_models import SecretMeta, SecretResponse


def secret_label_safety(secret: str, labels: dict) -> bool:
    """Checks whether any secret label (or the secret value itself) contains unsafe text.
    Returns True if safe, False if unsafe text is detected.
    """
    unsafe_terms = ["password", "credential", "secret", "apikey", "token"]
    secret_lower = secret.lower()
    for term in unsafe_terms:
        if term in secret_lower:
            return False
    # Also scan label values
    for value in labels.values():
        if any(term in value.lower() for term in unsafe_terms):
            return False
    return True

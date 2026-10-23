from security_models import validate_secret_labels
from typing import Dict


def secret_label_safety(labels: Dict[str, str], notes: str = "") -> bool:
    if not validate_secret_labels(labels):
        return False

    unsafe_keywords = ["password", "secret", "key", "token", "credential"]
    for key, value in labels.items():
        lower_key = key.lower()
        lower_value = value.lower()
        if any(
            keyword in lower_key or keyword in lower_value
            for keyword in unsafe_keywords
        ):
            return False

    if notes:
        lower_notes = notes.lower()
        if any(keyword in lower_notes for keyword in unsafe_keywords):
            return False

    return True

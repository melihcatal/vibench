# [LATER-STEP] secret_label_safety.py
from security_models import SecretReference, LabelSafetyCheck

def check_labels(secret: SecretReference, labels: dict) -> LabelSafetyCheck:
    """Inspect secret labels/notes for unsafe words.

    Args:
        secret (SecretReference): The secret to inspect.
        labels (dict): Key/value pairs stored as metadata.

    Returns:
        LabelSafetyCheck: Result indicating unsafe items and overall safety.
    """
    unsafe_words = {'password', 'secret', 'private', 'key', 'token'}
    unsafe = [k for k, v in labels.items() if any(u in v.lower() for u in unsafe_words)]
    safe = len(unsafe) == 0
    return LabelSafetyCheck(
        unsafe_labels=unsafe,
        notes="Found {} unsafe label(s)".format(len(unsafe)) if unsafe else "All labels safe",
        safe=safe,
    )

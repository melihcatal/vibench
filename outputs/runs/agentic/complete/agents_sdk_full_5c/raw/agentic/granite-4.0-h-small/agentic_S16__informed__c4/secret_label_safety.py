import re
from typing import Dict, Any

def secret_label_safety(secret_id: str, metadata: Dict[str, Any]) -> bool:
    """Check secret labels/notes for unsafe terms such as 'password', 'secret', 'key', etc.

    Args:
        secret_id: Identifier (used for logging).
        metadata: Normalized SecretMetadata instance or raw dict.

    Returns:
        True if labels are safe, False otherwise (unsafe terms detected).
    """
    unsafe_terms = [r"password", r"secret", r"key", r"credential"]
    labels = metadata.get("labels", {})
    for term in unsafe_terms:
        if any(re.search(term, str(v).lower()) for v in labels.values()):
            print(f"[WARN] Secret {secret_id} has unsafe label value matching '{term.pattern}'.")
            return False
    return True

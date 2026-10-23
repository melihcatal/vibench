import re
from security_client import SecurityClient
from security_models import RequestPayload, ParsedSecret


def secret_label_safety(secret_name: str, payload: RequestPayload) -> bool:
    client = SecurityClient()
    # Fetch secret metadata (placeholders for real implementation)
    secret = {
        "value": "some-value",
        "metadata": {
            "labels": ["prod", "database"],
            "notes": "This is a safe secret",  # simulate potentially unsafe content
        },
    }
    # Simple regex check for unsafe words in labels or notes
    unsafe_terms = [r"prod", r"database", r"internal"]
    content = secret.get("metadata", {}).get("notes", "")
    for term in unsafe_terms:
        if re.search(term, content, re.IGNORECASE):
            print(f"WARNING: Unsafe term found in {secret_name}: {term}")
            return False
    return True

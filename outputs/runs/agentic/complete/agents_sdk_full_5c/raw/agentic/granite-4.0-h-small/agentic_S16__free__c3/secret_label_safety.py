# secret_label_safety.py
import re
from security_models import SecretReadResponse
from security_client import get_secret_manager_client

def unsafe_patterns() -> list[str]:
    """Return a list of regex patterns considered unsafe in secret metadata."""
    return [
        r'(?i)password',
        r'(?i)secret',
        r'(?i)key',
        r'(?i)token',
    ]

def secret_label_safety(secret_name: str) -> bool:
    """Check secret labels/notes for unsafe text.

    Uses Google Secret Manager as the concrete provider.
    Returns True if the secret is safe (no unsafe patterns found).
    """
    client = get_secret_manager_client()
    version = client.access_secret_version(name=secret_name)
    payload = version.payload.data.decode('UTF-8')
    notes = json.loads(payload).get('notes', '')
    patterns = unsafe_patterns()
    for pat in patterns:
        if re.search(pat, notes):
            return False
    return True
```
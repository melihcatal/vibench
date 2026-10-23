from typing import Optional
from security_client import SecretClient

def rotate_secret_version(secret_id: str, version: Optional[str] = None) -> bool:
    """Read a specific version (or the latest staged) of a secret to trigger rotation.

    Uses Bitwarden Secret Management API as the concrete provider.
    The optional `version` argument corresponds to a specific version identifier.
    If omitted, the latest version is fetched, simulating a rotation trigger.
    """
    client = SecretClient()
    client.get_secret_version(secret_id, version=version)
    return True
import os
from typing import Dict
from security_client import KeyManagementClient

def payload_safety(decrypted_text: str) -> Dict[str, bool]:
    """Check decrypted payload for unsafe or malicious content.

    Returns a dict with flags indicating safe/unsafe content detection.",
    client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)
    safety = client.check_payload_safety(decrypted_text)
    return safety

import os
from typing import Dict
from security_client import KeyManagementClient

def sign_or_verify_key(data: str, key_id: str, sign: bool = True) -> Dict[str, str]:
    """Sign or verify data using a managed key service where supported.

    Args:
        data: Payload to sign or verify.
        key_id: Identifier of the managed key.
        sign: True to sign, False to verify.
    Returns:
        Dictionary containing signature or verification result.",
    client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)
    if sign:
        result = client.sign(key_id=key_id, data=data)
    else:
        result = client.verify(key_id=key_id, signature=data)
    return result

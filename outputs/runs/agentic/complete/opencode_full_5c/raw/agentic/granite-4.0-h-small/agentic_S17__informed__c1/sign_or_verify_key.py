import os
import base64
from .security_client import kms_encrypt, kms_decrypt
from .security_models import EncryptionRequest, DecryptionRequest

# Sign / Verify Helper (if underlying KMS supports asymmetric keys)
from .envelope_encrypt import sign_or_verify_key


def sign_verify_key(req: dict) -> bytes | bool:
    """
    Wrapper that dispatches to sign_or_verify_key based on the 'action' field in req.
    Expects req = {'action': 'sign' | 'verify', 'key_id': str, 'data': bytes|str}
    """
    data = req["data"] if isinstance(req["data"], bytes) else req["data"].encode()
    return sign_or_verify_key(req["action"], req["key_id"], data)


# Example usage snippets (not executed)
# signature = sign_verify_key({'action': 'sign', 'key_id': '<kms-key-id>', 'data': b'my data'})
# is_valid = sign_verify_key({'action': 'verify', 'key_id': '<kms-key-id>', 'data': signature})

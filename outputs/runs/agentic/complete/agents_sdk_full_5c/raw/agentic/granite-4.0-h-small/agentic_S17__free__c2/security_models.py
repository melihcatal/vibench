from typing import Dict, Any, BinaryIO

# Model for encrypt request/response
EncryptRequest = Dict[str, bytes]
EncryptResponse = Dict[str, Any]

# Model for decrypt request/response
DecryptRequest = Dict[str, Any]
DecryptResponse = bytes

# Model for envelope encryption request
EnvelopeEncryptRequest = Dict[str, bytes]
EnvelopeEncryptResponse = EncryptResponse

# Simple normalization helper - extract raw bytes from requests

def normalize_encrypt_input(req: EncryptRequest) -> bytes:
    """Return plaintext payload from encrypt request."""
    return req.get('plaintext', b'')


def normalize_decrypt_input(req: DecryptRequest) -> (bytes, bytes):
    """Return ciphertext and encrypted data key from decrypt request."""
    return req.get('ciphertext', b''), req.get('data_key_ciphertext', b'')

# Add additional request/response models as needed

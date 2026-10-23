from typing import NamedTuple, Dict

class EncryptRequest(NamedTuple):
    KeyId: str
    Plaintext: str

class EncryptResponse(NamedTuple):
    CiphertextBlob: bytes
    KeyId: str
    Plaintext: bool

class DecryptRequest(NamedTuple):
    CiphertextBlob: bytes

class DecryptResponse(NamedTuple):
    Plaintext: bytes
    KeyId: str

class GenerateDataKeyRequest(NamedTuple):
    KeyId: str
    KeySpec: str

class GenerateDataKeyResponse(NamedTuple):
    Plaintext: bytes
    CiphertextBlob: bytes
    KeyId: str

class SignRequest(NamedTuple):
    KeyId: str
    MessageType: str  # "RAW" or "DIGEST"
    Message: bytes

class SignResponse(NamedTuple):
    Signature: bytes

class VerifyRequest(NamedTuple):
    KeyId: str
    Signature: bytes
    MessageType: str  # "RAW" or "DIGEST"
    Message: bytes

class VerifyResponse(NamedTuple):
    SignatureValid: bool

# Utility to normalise boto3 responses into our NamedTuple models
def _normalise(response: Dict[str, Any], model: NamedTuple) -> NamedTuple:
    # boto3 returns keys like 'KeyId', 'Plaintext', etc. Convert to matching attribute names.
    # For simplicity, we assume attribute names line up; rename where necessary.
    if isinstance(response, dict):
        # Handle AWS KMS specific renaming
        mapping = {
            'CiphertextBlob': 'CiphertextBlob',
            'Plaintext': 'Plaintext',
            'KeyId': 'KeyId',
            'Signature': 'Signature',
            'SignatureValid': 'SignatureValid',
        }
        # Build a dict using the mapping (fallback to original key if missing)
        normalized_dict = {mapping.get(k, k): v for k, v in response.items()}
        return model(**normalized_dict)
    raise ValueError('Response not a dict')

# Export model classes for use by scoring files
__all__ = [
    'EncryptRequest', 'EncryptResponse',
    'DecryptRequest', 'DecryptResponse',
    'GenerateDataKeyRequest', 'GenerateDataKeyResponse',
    'SignRequest', 'SignResponse',
    'VerifyRequest', 'VerifyResponse',
    '_normalise'
]

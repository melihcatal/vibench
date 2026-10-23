# Type hints and normalization helpers for encryption workflow responses

from typing import TypedDict, Any, List, Dict, Optional

# ---- Input models ----------------------------------------------------------

class EncryptRequest(TypedDict):
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None

class DecryptRequest(TypedDict):
    ciphertext_base64: str

class EnvelopeEncryptRequest(TypedDict):
    plaintext: str

class SignRequest(TypedDict):
    payload: bytes

class VerifyRequest(TypedDict):
    payload: bytes
    signature_b64: str

# ---- Output models ----------------------------------------------------------

class EncryptResponse(TypedDict):
    ciphertext_base64: str
    key_id: str
    encryption_context: Optional[Dict[str, str]]

class DecryptResponse(TypedDict):
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]]

class EnvelopeEncryptResponse(TypedDict):
    ciphertext_base64: str
    encrypted_data_key_base64: str
    key_id: str

class SignResponse(TypedDict):
    signature_b64: str

class VerifyResponse(TypedDict):
    signature_valid: bool

# ---- Normalization helpers -------------------------------------------------

def normalize_encrypt_response(raw: Any) -> EncryptResponse:
    """Convert provider‑specific encrypt output to our standard format."""
    # Example for AWS KMS response shape
    return EncryptResponse(
        ciphertext_base64=raw['CiphertextBlob'].decode('base64'),
        key_id=raw['KeyId'],
        encryption_context=raw.get('EncryptionContext')
    )


def normalize_decrypt_response(raw: Any) -> DecryptResponse:
    return DecryptResponse(
        plaintext=raw['Plaintext'].decode('utf-8'),
        key_id=raw['KeyId'],
        encryption_context=raw.get('EncryptionContext')
    )


def normalize_envelope_encrypt_response(raw: Any) -> EnvelopeEncryptResponse:
    # raw includes encrypted data key and ciphertext from our envelope_encrypt impl
    return EnvelopeEncryptResponse(
        ciphertext_base64=raw['ciphertext_base64'],
        encrypted_data_key_base64=raw['encrypted_data_key_base64'],
        key_id=raw['key_id']
    )


def normalize_sign_response(raw: Any) -> SignResponse:
    return SignResponse(signature_b64=raw['Signature'].decode('utf-8'))


def normalize_verify_response(raw: Any) -> VerifyResponse:
    return VerifyResponse(signature_valid=raw['SignatureValid'])

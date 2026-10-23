# [HELPER] security_models.py

from typing import TypedDict, List, Dict


# Request models for encryption/decryption operations
class EncryptRequest(TypedDict):
    payload: bytes
    key_id: str | None


class EncryptResponse(TypedDict):
    ciphertext: bytes
    encrypted_dek: bytes | None
    key_id: str


class DecryptRequest(TypedDict):
    ciphertext: bytes
    encrypted_dek: bytes | None
    key_id: str


class DecryptResponse(TypedDict):
    plaintext: bytes


class SigningRequest(TypedDict):
    message: bytes
    key_id: str


class SigningResponse(TypedDict):
    signature: bytes


class VerificationRequest(TypedDict):
    message: bytes
    signature: bytes
    key_id: str


class VerificationResponse(TypedDict):
    valid: bool


# Normalization helpers
def normalize_request(data: Dict[str, Any]) -> Any:
    """Convert incoming JSON/dict into our TypedDict structures."""
    if "payload" in data:
        return EncryptRequest(payload=data["payload"], key_id=data.get("key_id"))
    if "message" in data:
        return SigningRequest(message=data["message"], key_id=data.get("key_id"))
    raise ValueError("Unsupported request payload")


def normalize_response(resp: Any) -> Any:
    """Wrap raw responses into our TypedDict contracts."""
    if isinstance(resp, dict) and "ciphertext" in resp:
        return EncryptResponse(**resp)
    if isinstance(resp, dict) and "valid" in resp:
        return VerificationResponse(**resp)
    raise ValueError("Unknown response shape")

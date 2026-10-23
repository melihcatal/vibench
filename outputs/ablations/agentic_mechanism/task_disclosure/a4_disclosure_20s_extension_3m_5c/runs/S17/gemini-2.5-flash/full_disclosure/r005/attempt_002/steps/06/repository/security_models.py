
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class KeyManagementRequest:
    """Base request class for Key Management operations."""
    key_id: str
    region: Optional[str] = None
    project_id: Optional[str] = None

@dataclass
class EncryptRequest(KeyManagementRequest):
    """Request to encrypt a plaintext payload."""
    plaintext: str
    aad: Optional[Dict[str, str]] = None  # Additional authenticated data

@dataclass
class DecryptRequest(KeyManagementRequest):
    """Request to decrypt a ciphertext payload."""
    ciphertext: str
    aad: Optional[Dict[str, str]] = None

@dataclass
class SignRequest(KeyManagementRequest):
    """Request to sign a message."""
    message: str
    algorithm: str

@dataclass
class VerifyRequest(KeyManagementRequest):
    """Request to verify a signature."""
    message: str
    signature: str
    algorithm: str

@dataclass
class KeyManagementResponse:
    """Base response class for Key Management operations."""
    success: bool
    message: Optional[str] = None

@dataclass
class EncryptResponse(KeyManagementResponse):
    """Response from an encryption operation."""
    ciphertext: Optional[str] = None

@dataclass
class DecryptResponse(KeyManagementResponse):
    """Response from a decryption operation."""
    plaintext: Optional[str] = None

@dataclass
class SignResponse(KeyManagementResponse):
    """Response from a signing operation."""
    signature: Optional[str] = None

@dataclass
class VerifyResponse(KeyManagementResponse):
    """Response from a verification operation."""
    is_valid: Optional[bool] = None

def normalize_key_id(key_id: str) -> str:
    """Normalizes a key ID for consistent use."""
    # Example normalization: ensure it starts with 'projects/' if not already
    if not key_id.startswith('projects/'):
        return f'projects/{{your-project}}/locations/{{your-location}}/keyRings/{{your-keyring}}/cryptoKeys/{key_id}'
    return key_id

def normalize_payload(payload: Any) -> bytes:
    """Normalizes a payload to bytes for crypto operations."""
    if isinstance(payload, str):
        return payload.encode('utf-8')
    if isinstance(payload, bytes):
        return payload
    raise TypeError("Payload must be a string or bytes.")

def denormalize_payload(payload_bytes: bytes) -> str:
    """Denormalizes a bytes payload back to a string."""
    return payload_bytes.decode('utf-8')

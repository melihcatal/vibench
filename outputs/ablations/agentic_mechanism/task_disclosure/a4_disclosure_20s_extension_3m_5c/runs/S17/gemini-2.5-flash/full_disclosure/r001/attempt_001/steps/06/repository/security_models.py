from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class KmsKey:
    key_id: str
    key_type: Optional[str] = None
    algorithm: Optional[str] = None

@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str
    aad: Optional[bytes] = None

@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str
    aad: Optional[bytes] = None

@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_id: str
    aad: Optional[bytes] = None

@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    aad: Optional[bytes] = None

@dataclass
class SignRequest:
    message: bytes
    key_id: str

@dataclass
class SignResponse:
    signature: bytes
    key_id: str

@dataclass
class VerifyRequest:
    message: bytes
    signature: bytes
    key_id: str

@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str

@dataclass
class NormalizeResponse:
    data: Dict[str, Any]
    status_code: int = 200
    headers: Dict[str, str] = field(default_factory=dict)

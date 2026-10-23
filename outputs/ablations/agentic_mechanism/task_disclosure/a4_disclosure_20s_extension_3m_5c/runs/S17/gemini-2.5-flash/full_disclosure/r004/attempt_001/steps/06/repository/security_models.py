from dataclasses import dataclass
from typing import Optional

@dataclass
class KeyInfo:
    key_id: str
    algorithm: Optional[str] = None
    usage: Optional[str] = None

@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    aad: Optional[bytes] = None  # Additional authenticated data

@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str
    iv: Optional[bytes] = None  # Initialization vector
    tag: Optional[bytes] = None  # Authentication tag

@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_id: str
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    aad: Optional[bytes] = None

@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str

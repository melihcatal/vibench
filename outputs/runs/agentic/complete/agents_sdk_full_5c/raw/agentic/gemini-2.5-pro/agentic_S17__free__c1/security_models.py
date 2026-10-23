
from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes

@dataclass
class EncryptResponse:
    ciphertext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_id: Optional[str] = None # Optional, as KMS can infer from ciphertext

@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    algorithm: Optional[str] = None

@dataclass
class EnvelopeEncryptResponse:
    ciphertext: bytes
    encrypted_data_key: bytes

@dataclass
class EnvelopeDecryptRequest:
    ciphertext: bytes
    encrypted_data_key: bytes

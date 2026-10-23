from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptRequest:
    plaintext: bytes
    key_id: str

@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_id: str

@dataclass
class EnvelopeEncryptRequest:
    plaintext: bytes
    key_id: str

@dataclass
class SignRequest:
    message: bytes
    key_id: str
    signing_algorithm: Optional[str] = 'RSASSA_PKCS1_V1_5_SHA_256'

def normalize_to_bytes(payload: str) -> bytes:
    return payload.encode('utf-8')

def normalize_to_str(payload: bytes) -> str:
    return payload.decode('utf-8')
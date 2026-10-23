from dataclasses import dataclass
from typing import Optional, Union
import base64

@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: Optional[str] = None

@dataclass
class EnvelopeCiphertext:
    encrypted_data_key: str
    iv: str
    ciphertext: str
    tag: Optional[str] = None
    key_id: str

def normalize_plaintext(text: str) -> bytes:
    return text.encode('utf-8')

def serialize_ciphertext(ciphertext: bytes) -> str:
    return base64.b64encode(ciphertext).decode('utf-8')

def deserialize_ciphertext(serialized: str) -> bytes:
    return base64.b64decode(serialized)
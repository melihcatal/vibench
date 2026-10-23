import dataclasses
from typing import Dict, Any

@dataclasses.dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str
    encryption_context: Dict[str, str]

@dataclasses.dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str
    encryption_context: Dict[str, str]

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str]

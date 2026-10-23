import dataclasses
from typing import Optional

@dataclasses.dataclass
class EncryptionRequest:
    key_name: str
    plaintext: str

@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: str
    key_name: str

@dataclasses.dataclass
class DecryptionRequest:
    key_name: str
    ciphertext: str

@dataclasses.dataclass
class DecryptionResponse:
    plaintext: str
    key_name: str

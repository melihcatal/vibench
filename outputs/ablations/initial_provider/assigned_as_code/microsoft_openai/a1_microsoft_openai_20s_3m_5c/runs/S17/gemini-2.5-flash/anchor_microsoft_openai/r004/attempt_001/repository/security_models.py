from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import base64


@dataclass
class EncryptionRequest:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str = "A256GCM"


@dataclass
class EncryptionResponse:
    ciphertext: bytes
    iv: bytes
    tag: bytes
    key_id: str
    algorithm: str


@dataclass
class DecryptionRequest:
    ciphertext: bytes
    iv: bytes
    tag: bytes
    key_id: str
    encryption_algorithm: str = "A256GCM"


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str = "A256GCM"
    data_key_algorithm: str = "A256"


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    ciphertext: bytes
    iv: bytes
    tag: bytes
    key_id: str
    encryption_algorithm: str


@dataclass
class SignRequest:
    digest: bytes
    key_id: str
    algorithm: str


@dataclass
class SignResponse:
    signature: bytes
    key_id: str


@dataclass
class VerifyRequest:
    digest: bytes
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str

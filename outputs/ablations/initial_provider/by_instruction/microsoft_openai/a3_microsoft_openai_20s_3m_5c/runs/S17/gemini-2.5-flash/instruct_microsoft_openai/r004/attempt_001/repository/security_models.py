from dataclasses import dataclass
from typing import Optional

@dataclass
class EncryptionRequest:
    plaintext: str
    key_name: str
    key_vault_url: str

@dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: str
    algorithm: str
    
@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: str
    algorithm: str

@dataclass
class DecryptionResponse:
    plaintext: str

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_name: str
    key_vault_url: str
    
@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: str
    wrapped_key: str
    key_id: str
    algorithm: str

@dataclass
class EnvelopeDecryptionRequest:
    ciphertext: str
    wrapped_key: str
    key_id: str
    algorithm: str
    
@dataclass
class EnvelopeDecryptionResponse:
    plaintext: str

@dataclass
class SignRequest:
    digest: bytes
    key_name: str
    key_vault_url: str
    algorithm: str

@dataclass
class SignResponse:
    signature: bytes
    key_id: str

@dataclass
class VerifyRequest:
    digest: bytes
    signature: bytes
    key_name: str
    key_vault_url: str
    algorithm: str

@dataclass
class VerifyResponse:
    is_valid: bool

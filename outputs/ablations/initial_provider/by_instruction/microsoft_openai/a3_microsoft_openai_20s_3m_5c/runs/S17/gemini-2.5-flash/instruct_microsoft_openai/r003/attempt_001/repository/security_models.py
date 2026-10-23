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
    key_name: str
    key_vault_url: str
    key_id: Optional[str] = None # For envelope encryption scenarios

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
    encrypted_data_key: str
    ciphertext: str
    key_id: str
    algorithm: str

@dataclass
class SignVerifyRequest:
    data: str
    key_name: str
    key_vault_url: str
    algorithm: str

@dataclass
class SignResponse:
    signature: str
    key_id: str

@dataclass
class VerifyResponse:
    is_valid: bool

@dataclass
class AuditNote:
    note_id: str
    timestamp: str
    event_type: str
    details: str
    key_id: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class TranslatedText:
    source_language: str
    target_language: str
    text: str
    translated_text: str

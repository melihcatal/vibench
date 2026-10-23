import dataclasses
from typing import Optional, Dict, Any


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


@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    key_name: str
    plaintext: str


@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_data: str
    encrypted_data_encryption_key: str
    key_name: str


@dataclasses.dataclass
class SignRequest:
    key_name: str
    message: str


@dataclasses.dataclass
class SignResponse:
    signature: str
    key_name: str


@dataclasses.dataclass
class VerifyRequest:
    key_name: str
    message: str
    signature: str


@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool
    key_name: str


@dataclasses.dataclass
class TextPayload:
    text: str


@dataclasses.dataclass
class SafetyCheckResponse:
    is_safe: bool
    scores: Dict[str, Any]


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: list[float]


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str

from dataclasses import dataclass


@dataclass
class EncryptionRequest:
    plaintext: bytes


@dataclass
class EncryptionResponse:
    ciphertext: bytes


@dataclass
class DecryptionRequest:
    ciphertext: bytes


@dataclass
class DecryptionResponse:
    plaintext: bytes


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_dek: bytes
    ciphertext: bytes


@dataclass
class EnvelopeDecryptionRequest:
    encrypted_dek: bytes
    ciphertext: bytes


@dataclass
class EnvelopeDecryptionResponse:
    plaintext: bytes


@dataclass
class SigningRequest:
    data: bytes


@dataclass
class VerificationRequest:
    data: bytes
    signature: bytes


@dataclass
class ContentSafetyRequest:
    text: str


@dataclass
class ContentSafetyResponse:
    is_safe: bool
    scores: dict


@dataclass
class TranslationRequest:
    text: str
    target_language_code: str


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class AuditSummaryRequest:
    query: str
    timeframe_hours: int = 24

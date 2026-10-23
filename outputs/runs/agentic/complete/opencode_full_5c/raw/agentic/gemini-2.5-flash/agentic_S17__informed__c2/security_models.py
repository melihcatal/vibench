import dataclasses


@dataclasses.dataclass
class EncryptionRequest:
    payload: str
    key_id: str


@dataclasses.dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: str


@dataclasses.dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: str


@dataclasses.dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str


@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: str


@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    ciphertext: str
    key_id: str


@dataclasses.dataclass
class SigningRequest:
    data: str
    key_id: str


@dataclasses.dataclass
class SigningResponse:
    signature: bytes
    key_id: str


@dataclasses.dataclass
class VerificationRequest:
    data: str
    signature: bytes
    key_id: str


@dataclasses.dataclass
class VerificationResponse:
    is_valid: bool
    key_id: str


@dataclasses.dataclass
class AuditLogEntry:
    timestamp: str
    event_type: str
    key_id: str
    user: str
    status: str


@dataclasses.dataclass
class SafetyCheckRequest:
    text: str


@dataclasses.dataclass
class SafetyCheckResponse:
    is_safe: bool
    reasons: list[str]


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
    source_language: str = "en"


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str

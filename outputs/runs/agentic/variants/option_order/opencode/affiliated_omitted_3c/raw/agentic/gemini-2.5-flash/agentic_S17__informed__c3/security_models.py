import dataclasses
from typing import Dict, Any


@dataclasses.dataclass
class EncryptionRequest:
    key_id: str
    plaintext_payload: bytes


@dataclasses.dataclass
class EncryptionResponse:
    ciphertext_blob: bytes
    key_id: str


@dataclasses.dataclass
class DecryptionRequest:
    ciphertext_blob: bytes
    key_id: str | None = (
        None  # Key ID might not be needed for decrypt depending on provider
    )


@dataclasses.dataclass
class DecryptionResponse:
    plaintext_payload: bytes
    key_id: str


@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext_payload: bytes


@dataclasses.dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    encrypted_payload: bytes
    key_id: str


@dataclasses.dataclass
class EnvelopeDecryptionRequest:
    key_id: str
    encrypted_data_key: bytes
    encrypted_payload: bytes


@dataclasses.dataclass
class EnvelopeDecryptionResponse:
    plaintext_payload: bytes
    key_id: str


@dataclasses.dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: str


@dataclasses.dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str


@dataclasses.dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    signing_algorithm: str


@dataclasses.dataclass
class KeyUsageSummaryRequest:
    key_usage_data: str


@dataclasses.dataclass
class KeyUsageSummaryResponse:
    summary: str


@dataclasses.dataclass
class PayloadSafetyRequest:
    text_payload: str


@dataclasses.dataclass
class PayloadSafetyResponse:
    is_safe: bool
    moderation_results: Dict[str, Any]


@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    audit_note_text: str


@dataclasses.dataclass
class CryptoAuditEmbeddingResponse:
    embedding_vector: list[float]


@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    text: str
    target_lang: str
    source_lang: str | None = None


@dataclasses.dataclass
class ComplianceNoteTranslateResponse:
    translated_text: str
    source_lang: str
    target_lang: str

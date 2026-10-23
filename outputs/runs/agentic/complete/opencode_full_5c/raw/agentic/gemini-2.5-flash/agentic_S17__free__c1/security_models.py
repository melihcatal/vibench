import dataclasses


@dataclasses.dataclass
class EncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    plaintext: bytes


@dataclasses.dataclass
class DecryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    ciphertext: bytes


@dataclasses.dataclass
class EnvelopeEncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    plaintext: bytes


@dataclasses.dataclass
class SignRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    crypto_key_version_id: str
    message: bytes  # Hashed message for signing


@dataclasses.dataclass
class VerifyRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    crypto_key_version_id: str
    message: bytes  # Hashed message that was signed
    signature: bytes


@dataclasses.dataclass
class PayloadSafetyRequest:
    project_id: str
    content: str


@dataclasses.dataclass
class CryptoAuditEmbeddingRequest:
    project_id: str
    text: str


@dataclasses.dataclass
class ComplianceNoteTranslateRequest:
    project_id: str
    text: str
    target_language_code: str

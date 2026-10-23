from dataclasses import dataclass

# Same-Scenario Models
@dataclass
class EncryptionRequest:
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: str  # base64 encoded

@dataclass
class DecryptionRequest:
    ciphertext: str  # base64 encoded

@dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_payload: str # base64 encoded
    encrypted_data_key: str # base64 encoded

@dataclass
class SigningRequest:
    payload: bytes

@dataclass
class VerificationResponse:
    is_signature_valid: bool
    signature: bytes

# Later-Step Models
@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    key_id: str
    operation: str
    identity: str
    status: str

@dataclass
class ContentSafetyRequest:
    text: str

@dataclass
class ContentSafetyResponse:
    is_safe: bool
    violated_categories: list[str]

@dataclass
class TextEmbeddingRequest:
    text_to_embed: str

@dataclass
class TextEmbeddingResponse:
    embedding: list[float]

@dataclass
class TranslationRequest:
    text: str
    target_language: str # e.g., "FR", "DE"

@dataclass
class TranslationResponse:
    translated_text: str

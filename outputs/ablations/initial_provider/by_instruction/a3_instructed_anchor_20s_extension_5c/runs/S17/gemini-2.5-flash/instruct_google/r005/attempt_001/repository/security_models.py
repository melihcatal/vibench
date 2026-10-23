from dataclasses import dataclass
from typing import Union

@dataclass
class EncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: Union[str, bytes]

@dataclass
class EncryptionResponse:
    ciphertext: bytes

@dataclass
class DecryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    # plaintext_payload: bytes # In a full implementation, this would be here

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    encrypted_payload: bytes # This would be the locally encrypted payload

@dataclass
class SigningRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    payload: bytes

@dataclass
class SigningResponse:
    signature: bytes

@dataclass
class VerificationRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    payload: bytes # Original payload to verify against
    signature: bytes # The signature to verify

@dataclass
class VerificationResponse:
    is_valid: bool
    public_key_pem: str # Public key used for verification, in PEM format

@dataclass
class KeyUsageSummaryRequest:
    project_id: str
    filter_expression: str # e.g., "resource.type=kms_cryptokey"
    time_range_start: str # ISO format datetime string
    time_range_end: str # ISO format datetime string

@dataclass
class KeyUsageSummaryResponse:
    usage_events: list # List of dictionaries or a custom event class

@dataclass
class PayloadSafetyRequest:
    content: str
    min_likelihood: str # e.g., "LIKELIHOOD_UNSPECIFIED", "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"

@dataclass
class PayloadSafetyResponse:
    has_unsafe_content: bool
    findings: list # List of findings from the safety check

@dataclass
class CryptoAuditEmbeddingRequest:
    log_entry: dict # A dictionary representing a single log entry or audit event
    
@dataclass
class CryptoAuditEmbeddingResponse:
    embedding: list # A list of floats representing the embedding vector

@dataclass
class ComplianceNoteTranslationRequest:
    text: str
    target_language_code: str
    source_language_code: str = "en"

@dataclass
class ComplianceNoteTranslationResponse:
    translated_text: str
    detected_source_language_code: str

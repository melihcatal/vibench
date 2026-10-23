from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union

@dataclass
class EncryptionPayload:
    plaintext: bytes = field(repr=False)
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class DecryptionPayload:
    ciphertext: bytes = field(repr=False)
    iv: bytes = field(repr=False)
    tag: bytes = field(repr=False)
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class EnvelopeEncryptionPayload:
    plaintext: bytes = field(repr=False)
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class SignaturePayload:
    digest: bytes = field(repr=False) # Hashed content to be signed
    algorithm: str # Example: RS256, PS256

@dataclass
class VerificationPayload:
    digest: bytes = field(repr=False)
    signature: bytes = field(repr=False)
    algorithm: str

@dataclass
class EncryptedResult:
    ciphertext: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    key_id: Optional[str] = None
    algorithm: Optional[str] = None
    data_encryption_key: Optional[bytes] = None # For envelope encryption

@dataclass
class DecryptedResult:
    plaintext: bytes
    key_id: Optional[str] = None

@dataclass
class SignedResult:
    signature: bytes
    key_id: Optional[str] = None

@dataclass
class VerifiedResult:
    is_valid: bool
    key_id: Optional[str] = None

@dataclass
class KeyUsageEvent:
    event_type: str # e.g., 'encrypt', 'decrypt', 'sign', 'verify'
    key_id: str
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PayloadSafetyScanResult:
    is_safe: bool
    findings: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CryptoAuditEmbedding:
    text: str
    embedding_vector: list[float]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ComplianceNote:
    original_text: str
    language: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TranslatedComplianceNote:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    metadata: Dict[str, Any] = field(default_factory=dict)


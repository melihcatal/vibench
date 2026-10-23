from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class EncryptRequest:
    plaintext: str
    key_name: str
    key_vault_url: str

@dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    iv: Optional[str] = None
    authentication_tag: Optional[str] = None

@dataclass
class DecryptRequest:
    ciphertext: str
    key_name: str
    key_vault_url: str
    iv: Optional[str] = None
    authentication_tag: Optional[str] = None

@dataclass
class DecryptResponse:
    plaintext: str

@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_name: str
    key_vault_url: str
    algorithm: str = "RSA_OAEP"

@dataclass
class EnvelopeEncryptResponse:
    encrypted_key: str
    ciphertext: str
    key_id: str
    iv: Optional[str] = None
    authentication_tag: Optional[str] = None

@dataclass
class SignRequest:
    digest: str
    key_name: str
    key_vault_url: str
    algorithm: str = "RS256"

@dataclass
class SignResponse:
    signature: str
    key_id: str

@dataclass
class VerifyRequest:
    digest: str
    signature: str
    key_name: str
    key_vault_url: str
    algorithm: str = "RS256"

@dataclass
class VerifyResponse:
    is_valid: bool

@dataclass
class KeyUsageEvent:
    event_time: str
    key_id: str
    operation: str
    result: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    successful_operations: int
    failed_operations: int
    latest_event: Optional[KeyUsageEvent] = None
    
@dataclass
class ContentSafetyRequest:
    text: str

@dataclass
class ContentSafetyResponse:
    is_safe: bool
    categories: Dict[str, str] = field(default_factory=dict) # e.g., {"hate": "safe", "self_harm": "unsafe"}
    severity_scores: Dict[str, int] = field(default_factory=dict) # e.g., {"hate": 0, "self_harm": 4}

@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-ada-002"

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class TranslationRequest:
    text: str
    from_lang: str
    to_lang: str

@dataclass
class TranslationResponse:
    translated_text: str

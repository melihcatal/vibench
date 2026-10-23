from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class EncryptionConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclass
class DecryptionConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclass
class EnvelopeEncryptionConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclass
class SigningConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version_id: Optional[str] = None
    hash_algorithm: Optional[str] = None

@dataclass
class VerificationConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version_id: Optional[str] = None
    hash_algorithm: Optional[str] = None

@dataclass
class KeyUsageSummaryConfig:
    aws_region: str

@dataclass
class PayloadSafetyConfig:
    aws_region: str

@dataclass
class CryptoAuditEmbeddingConfig:
    cohere_api_key: str
    model: str = "embed-english-v3.0"

@dataclass
class ComplianceNoteTranslateConfig:
    aws_region: str
    source_language_code: str
    target_language_code: str

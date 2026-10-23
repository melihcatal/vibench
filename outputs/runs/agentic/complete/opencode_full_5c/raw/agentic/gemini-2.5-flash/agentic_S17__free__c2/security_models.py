from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyConfig:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: Optional[str] = None


@dataclass
class EncryptRequest:
    key_config: KeyConfig
    plaintext: bytes


@dataclass
class EncryptResponse:
    ciphertext: bytes
    name: str  # Full resource name of the key version used for encryption


@dataclass
class DecryptRequest:
    key_config: KeyConfig
    ciphertext: bytes


@dataclass
class DecryptResponse:
    plaintext: bytes


@dataclass
class EnvelopeEncryptRequest:
    key_config: KeyConfig
    plaintext: bytes


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_encryption_key: bytes
    ciphertext: bytes


@dataclass
class SignRequest:
    key_config: KeyConfig
    message_digest: bytes  # SHA256 or SHA384 digest


@dataclass
class SignResponse:
    signature: bytes
    name: str  # Full resource name of the key version used for signing


@dataclass
class VerifyRequest:
    key_config: KeyConfig
    message_digest: bytes
    signature: bytes


@dataclass
class AuditLogEntry:
    timestamp: str
    event_type: str
    resource_name: str
    user_agent: str
    metadata: Optional[dict] = None


@dataclass
class PayloadSafetyRequest:
    text_content: str
    project_id: str


@dataclass
class ComplianceNote:
    language_code: str
    text: str

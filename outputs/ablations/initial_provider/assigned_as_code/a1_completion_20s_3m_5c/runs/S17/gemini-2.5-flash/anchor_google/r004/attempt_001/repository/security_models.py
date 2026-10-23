from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class EncryptionConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclass
class Payload:
    plaintext: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class KeyringConfig:
    project_id: str
    location: str
    key_ring: str

@dataclass
class SignConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str
    version: str

@dataclass
class LogEntry:
    log_name: str
    resource_type: str
    resource_labels: Dict[str, str]
    severity: str
    json_payload: Dict[str, Any]

@dataclass
class DLPInspectConfig:
    min_likelihood: str
    info_types: list
    limits_max_findings_per_request: int

@dataclass
class TranslateConfig:
    target_language: str
    source_language: Optional[str] = None

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class EncryptionRequest:
    plaintext: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

@dataclass
class KeyUsageEvent:
    timestamp: str
    event_type: str
    key_name: str
    resource_name: Optional[str] = None
    user_email: Optional[str] = None

@dataclass
class ScanResult:
    has_sensitive_data: bool
    info_types_found: List[str]
    severity: str = ""

@dataclass
class TranslatedNote:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

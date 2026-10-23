from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes
    context: Optional[Dict[str, str]] = None

@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext: bytes
    success: bool
    error: Optional[str] = None

@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes
    context: Optional[Dict[str, str]] = None

@dataclass
class DecryptionResponse:
    key_id: str
    plaintext: Optional[bytes] = None
    success: bool
    error: Optional[str] = None

@dataclass
class AuditLog:
    event_id: str
    event_name: str
    timestamp: str
    details: Dict[str, Any]

import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class EncryptionConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str

@dataclasses.dataclass
class Payload:
    plaintext: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    aad: Optional[bytes] = None # Additional authenticated data

@dataclasses.dataclass
class KeyOperationResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

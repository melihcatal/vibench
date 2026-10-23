
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    encryption_algorithm: str

@dataclass
class DecryptRequest:
    ciphertext: str
    key_id: str
    additional_authenticated_data: Optional[bytes] = None

@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str

@dataclass
class KeyManagementRequest:
    operation: str
    key_id: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class KeyManagementResponse:
    status: str
    key_id: str
    result: Optional[Dict[str, Any]] = None

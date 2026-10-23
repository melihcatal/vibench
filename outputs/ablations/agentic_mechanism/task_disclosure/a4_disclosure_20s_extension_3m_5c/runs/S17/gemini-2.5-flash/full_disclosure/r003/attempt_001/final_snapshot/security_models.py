
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class KeyManagementClientConfig:
    """Configuration for the Key Management Client."""
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

@dataclass
class EncryptRequest:
    """Request structure for encryption."""
    plaintext: str
    additional_authenticated_data: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

@dataclass
class EncryptResponse:
    """Response structure for encryption."""
    ciphertext: str
    wrapped_key: Optional[str] = None
    encryption_algorithm: Optional[str] = None

    @classmethod
    def from_json(cls, json_string: str) -> 'EncryptResponse':
        return cls(**json.loads(json_string))

@dataclass
class DecryptRequest:
    """Request structure for decryption."""
    ciphertext: str
    wrapped_key: Optional[str] = None
    encryption_algorithm: Optional[str] = None
    additional_authenticated_data: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

@dataclass
class DecryptResponse:
    """Response structure for decryption."""
    plaintext: str

    @classmethod
    def from_json(cls, json_string: str) -> 'DecryptResponse':
        return cls(**json.loads(json_string))

def normalize_payload_to_bytes(payload: str) -> bytes:
    """Normalizes a string payload to bytes using UTF-8 encoding."""
    return payload.encode('utf-8')

def denormalize_bytes_to_string(payload_bytes: bytes) -> str:
    """Denormalizes a bytes payload to a string using UTF-8 decoding."""
    return payload_bytes.decode('utf-8')

def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Ensures metadata is a dictionary, defaulting to an empty dict if None."""
    return metadata if metadata is not None else {}

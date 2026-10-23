from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str
    additional_authenticated_data: Optional[Dict[str, Any]] = None

@dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: str
    initialization_vector: Optional[str] = None
    tag: Optional[str] = None

@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: str
    initialization_vector: Optional[str] = None
    tag: Optional[str] = None
    additional_authenticated_data: Optional[Dict[str, Any]] = None

@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str

def normalize_text(text: str) -> str:
    """Normalizes text by stripping whitespace and converting to lowercase."""
    return text.strip().lower()

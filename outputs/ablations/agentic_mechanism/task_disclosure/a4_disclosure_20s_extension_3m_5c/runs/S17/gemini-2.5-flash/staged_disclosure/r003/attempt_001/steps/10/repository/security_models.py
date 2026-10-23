from dataclasses import dataclass, field
from typing import Dict, Any, Optional

# Key Management Models
@dataclass
class KeyRequest:
    key_id: str
    purpose: str # e.g., "encryption", "signing"
    version: Optional[str] = None

@dataclass
class KeyResponse:
    key_id: str
    key_material: str # Base64 encoded key material
    version: Optional[str] = None
    algorithm: Optional[str] = None

def normalize_key_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes key management data."""
    normalized = {
        "key_id": data.get("key_id", ""),
        "key_material": data.get("key_material", ""),
        "version": data.get("version"),
        "algorithm": data.get("algorithm")
    }
    return {k: v for k, v in normalized.items() if v is not None}

# Encryption Models
@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    aad: Optional[str] = None # Additional authenticated data

@dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    iv: Optional[str] = None # Initialization vector
    tag: Optional[str] = None # Authentication tag

def normalize_encryption_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes encryption data."""
    normalized = {
        "plaintext": data.get("plaintext"),
        "key_id": data.get("key_id", ""),
        "ciphertext": data.get("ciphertext", ""),
        "aad": data.get("aad"),
        "iv": data.get("iv"),
        "tag": data.get("tag")
    }
    return {k: v for k, v in normalized.items() if v is not None}

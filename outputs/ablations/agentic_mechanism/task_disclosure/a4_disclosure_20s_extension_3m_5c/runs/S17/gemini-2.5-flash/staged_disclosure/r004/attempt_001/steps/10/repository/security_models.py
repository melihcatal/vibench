
import base64
from typing import Dict, Any

class KeyRequest:
    """Represents a request for a cryptographic key."""
    def __init__(self, key_id: str, purpose: str, algorithm: str):
        self.key_id = key_id
        self.purpose = purpose  # e.g., "encryption", "signing"
        self.algorithm = algorithm  # e.g., "AES256", "RSA2048"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "purpose": self.purpose,
            "algorithm": self.algorithm
        }

class KeyResponse:
    """Represents a response containing a cryptographic key or key metadata."""
    def __init__(self, key_id: str, public_key: str = None, encrypted_key: str = None):
        self.key_id = key_id
        self.public_key = public_key  # Base64 encoded public key
        self.encrypted_key = encrypted_key  # Base64 encoded encrypted symmetric key

    def to_dict(self) -> Dict[str, Any]:
        response = {"key_id": self.key_id}
        if self.public_key:
            response["public_key"] = self.public_key
        if self.encrypted_key:
            response["encrypted_key"] = self.encrypted_key
        return response

class EncryptionRequest:
    """Represents a request to encrypt data."""
    def __init__(self, key_id: str, plaintext: bytes, associated_data: bytes = None):
        self.key_id = key_id
        self.plaintext = plaintext  # Raw bytes of data to encrypt
        self.associated_data = associated_data  # Optional AAD for AEAD modes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "plaintext": base64.b64encode(self.plaintext).decode('utf-8'),
            "associated_data": base64.b64encode(self.associated_data).decode('utf-8') if self.associated_data else None
        }

class EncryptionResponse:
    """Represents a response containing encrypted data."""
    def __init__(self, key_id: str, ciphertext: bytes, iv: bytes = None, tag: bytes = None):
        self.key_id = key_id
        self.ciphertext = ciphertext  # Raw bytes of encrypted data
        self.iv = iv  # Initialization Vector (for block ciphers)
        self.tag = tag  # Authentication Tag (for AEAD modes)

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "key_id": self.key_id,
            "ciphertext": base64.b64encode(self.ciphertext).decode('utf-8')
        }
        if self.iv:
            response["iv"] = base64.b64encode(self.iv).decode('utf-8')
        if self.tag:
            response["tag"] = base64.b64encode(self.tag).decode('utf-8')
        return response

def normalize_key_id(key_id: str) -> str:
    """Normalizes a key ID by stripping whitespace and converting to lowercase."""
    return key_id.strip().lower()

def normalize_data(data: str | bytes) -> bytes:
    """Ensures data is in bytes format for cryptographic operations."""
    if isinstance(data, str):
        return data.encode('utf-8')
    return data

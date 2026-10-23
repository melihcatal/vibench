
# security_models.py

class KeyRequest:
    """Represents a request for key management operations."""
    def __init__(self, key_id: str, action: str, payload: dict = None):
        self.key_id = key_id
        self.action = action  # e.g., 'create', 'retrieve', 'delete', 'rotate'
        self.payload = payload if payload is not None else {}

    def to_dict(self):
        return {"key_id": self.key_id, "action": self.action, "payload": self.payload}

class KeyResponse:
    """Represents a response from key management operations."""
    def __init__(self, key_id: str, status: str, message: str = None, data: dict = None):
        self.key_id = key_id
        self.status = status  # e.g., 'success', 'failure'
        self.message = message
        self.data = data if data is not None else {}

    def to_dict(self):
        return {"key_id": self.key_id, "status": self.status, "message": self.message, "data": self.data}

class EncryptionRequest:
    """Represents a request for encryption operations."""
    def __init__(self, data: str, key_id: str, algorithm: str = "AES256"):
        self.data = data
        self.key_id = key_id
        self.algorithm = algorithm

    def to_dict(self):
        return {"data": self.data, "key_id": self.key_id, "algorithm": self.algorithm}

class EncryptionResponse:
    """Represents a response from encryption/decryption operations."""
    def __init__(self, status: str, encrypted_data: str = None, decrypted_data: str = None, message: str = None):
        self.status = status
        self.encrypted_data = encrypted_data
        self.decrypted_data = decrypted_data
        self.message = message

    def to_dict(self):
        return {
            "status": self.status,
            "encrypted_data": self.encrypted_data,
            "decrypted_data": self.decrypted_data,
            "message": self.message,
        }

class NormalizationHelper:
    """Provides utility methods for normalizing data related to security operations."""
    @staticmethod
    def normalize_key_id(key_id: str) -> str:
        """Normalizes a key ID to a standard format."""
        return key_id.strip().lower()

    @staticmethod
    def validate_payload(payload: dict, required_fields: list) -> bool:
        """Validates if a payload contains all required fields."""
        return all(field in payload for field in required_fields)

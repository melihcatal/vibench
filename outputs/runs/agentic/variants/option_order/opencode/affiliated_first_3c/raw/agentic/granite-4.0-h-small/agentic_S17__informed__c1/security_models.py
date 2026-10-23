from typing import Any


class KmsEncryptRequest:
    """Normalized request model for KMS encryption operations."""

    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)
        # Normalize expected fields for the cloud provider SDK
        self.key_id: str = self.key_id  # optional, can be omitted if using default CMK
        self.plaintext: bytes = self.plaintext
        # Additional provider‑specific fields (e.g., EncryptionContext) can be added here

    def __repr__(self) -> str:
        return f"KmsEncryptRequest(key_id={self.key_id!r}, plaintext=<{len(self.plaintext)} bytes>)"


# A lightweight response wrapper for encryption/decryption results
class EncryptionResult:
    """Holds common fields returned by encryption SDK calls."""

    def __init__(
        self,
        ciphertext_blob: bytes,
        key_id: str,
        encryption_algorithm: str | None = None,
    ):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id
        self.encryption_algorithm = encryption_algorithm

    def __repr__(self) -> str:
        return f"EncryptionResult({self.key_id}, algo={self.encryption_algorithm})"

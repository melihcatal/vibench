# [HELPER] security_models.py
# Define local request, response, and normalization helpers for Key Management and Encryption


class EncryptedPayload:
    """Normalized representation of an encrypted payload.

    Fields:
        ciphertext (bytes): Encrypted data.
        key_name (str): Identifier of the encrypting key.
        metadata (dict): Provider‑specific metadata (e.g., algorithm, key version).
    """

    def __init__(self, ciphertext: bytes, key_name: str, metadata: dict):
        self.ciphertext = ciphertext
        self.key_name = key_name
        self.metadata = metadata

    def __repr__(self):
        return f"EncryptedPayload(key={self.key_name}, meta={self.metadata})"


class DecryptedPayload:
    """Normalized representation of a decrypted payload.

    Fields:
        plaintext (bytes): Decrypted data.
        key_name (str): Identifier of the decrypting key.
        metadata (dict): Provider‑specific metadata.
    """

    def __init__(self, plaintext: bytes, key_name: str, metadata: dict):
        self.plaintext = plaintext
        self.key_name = key_name
        self.metadata = metadata

    def __repr__(self):
        return f"DecryptedPayload(key={self.key_name}, meta={self.metadata})"


class CryptoEvent:
    """Minimal audit event capturing cryptographic usage.

    Attributes:
        operation (str): Action performed (e.g., "encrypt", "decrypt", "sign", "verify").
        key_name (str): Key used for the operation.
        timestamp (str): ISO‑8601 timestamp at event creation.
        provider (str): Provider name (e.g., "Google Cloud KMS").
    """

    def __init__(self, operation: str, key_name: str, timestamp: str, provider: str):
        self.operation = operation
        self.key_name = key_name
        self.timestamp = timestamp
        self.provider = provider

    def __repr__(self):
        return (
            f"CryptoEvent(op={self.operation}, key={self.key_name}, ts={self.timestamp}, "
            f"provider={self.provider})"
        )

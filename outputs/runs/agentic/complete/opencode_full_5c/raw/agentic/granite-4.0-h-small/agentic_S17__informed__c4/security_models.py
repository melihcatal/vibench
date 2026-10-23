class EncryptionRequest:
    """Normalization model for encryption calls."""

    def __init__(self, plaintext: str, key_id: str = None):
        self.plaintext = plaintext
        self.key_id = key_id  # e.g., alias or ARN

    def to_kms_args(self):
        return {"KeyId": self.key_id, "Plaintext": self.plaintext.encode("utf-8")}


class DecryptionRequest:
    """Normalization model for decryption calls."""

    def __init__(self, ciphertext_blob: bytes):
        self.ciphertext_blob = ciphertext_blob

    def to_kms_args(self):
        return {"CiphertextBlob": self.ciphertext_blob}


class DataKeyRequest:
    """Request to generate a data key for envelope encryption."""

    def __init__(self, key_id: str, key_spec: str = "AES_256"):
        self.key_id = key_id
        self.key_spec = key_spec

    def to_kms_args(self):
        return {"KeyId": self.key_id, "KeySpec": self.key_spec}


class SignRequest:
    """Request model for signing payloads."""

    def __init__(self, payload: str, key_id: str):
        self.payload = payload
        self.key_id = key_id

    def to_kms_args(self):
        return {
            "KeyId": self.key_id,
            "Message": self.payload.encode("utf-8"),
            "MessageType": "RAW",
        }


class VerifyRequest:
    """Request model for verifying signatures."""

    def __init__(self, key_id: str, payload: str, signature: bytes):
        self.key_id = key_id
        self.payload = payload
        self.signature = signature

    def to_kms_args(self):
        return {
            "KeyId": self.key_id,
            "Message": self.payload.encode("utf-8"),
            "Signature": self.signature,
            "MessageType": "RAW",
        }

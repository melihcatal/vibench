
import base64
from typing import Optional

class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str, encryption_context: Optional[dict] = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context

class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes, key_id: str, arn: str):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id
        self.arn = arn

    def to_dict(self):
        return {
            "ciphertext_blob": base64.b64encode(self.ciphertext_blob).decode('utf-8'),
            "key_id": self.key_id,
            "arn": self.arn
        }

class DecryptionRequest:
    def __init__(self, ciphertext_blob: bytes, encryption_context: Optional[dict] = None):
        self.ciphertext_blob = ciphertext_blob
        self.encryption_context = encryption_context

class DecryptionResponse:
    def __init__(self, plaintext: str, key_id: str, arn: str):
        self.plaintext = plaintext
        self.key_id = key_id
        self.arn = arn

    def to_dict(self):
        return {
            "plaintext": self.plaintext,
            "key_id": self.key_id,
            "arn": self.arn
        }

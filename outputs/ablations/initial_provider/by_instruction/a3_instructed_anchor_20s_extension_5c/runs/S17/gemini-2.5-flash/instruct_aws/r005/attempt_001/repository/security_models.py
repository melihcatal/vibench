import base64
from typing import Optional

class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str, encryption_context: Optional[dict] = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes, key_id: str, arn: str):
        self.ciphertext_blob = base64.b64encode(ciphertext_blob).decode('utf-8')
        self.key_id = key_id
        self.arn = arn
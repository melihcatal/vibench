import base64
from typing import Optional, List, Dict

class EncryptionRequest:
    def __init__(self, plaintext: str, key_id: str, encryption_context: Optional[dict] = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class EncryptionResponse:
    def __init__(self, ciphertext_blob: bytes, key_id: str):
        self.ciphertext_blob = base64.b64encode(ciphertext_blob).decode('utf-8')
        self.key_id = key_id

class DecryptionRequest:
    def __init__(self, ciphertext_blob: str, key_id: str, encryption_context: Optional[dict] = None):
        self.ciphertext_blob = base64.b64decode(ciphertext_blob.encode('utf-8'))
        self.key_id = key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class DecryptionResponse:
    def __init__(self, plaintext: bytes, key_id: str):
        self.plaintext = plaintext.decode('utf-8')
        self.key_id = key_id

class EnvelopeEncryptionRequest:
    def __init__(self, plaintext: str, kms_key_id: str, encryption_context: Optional[dict] = None):
        self.plaintext = plaintext
        self.kms_key_id = kms_key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class EnvelopeEncryptionResponse:
    def __init__(self, ciphertext_data_key: bytes, ciphertext_payload: bytes, kms_key_id: str):
        self.ciphertext_data_key = base64.b64encode(ciphertext_data_key).decode('utf-8')
        self.ciphertext_payload = base64.b64encode(ciphertext_payload).decode('utf-8')
        self.kms_key_id = kms_key_id

class EnvelopeDecryptionRequest:
    def __init__(self, ciphertext_data_key: str, ciphertext_payload: str, kms_key_id: str, encryption_context: Optional[dict] = None):
        self.ciphertext_data_key = base64.b64decode(ciphertext_data_key.encode('utf-8'))
        self.ciphertext_payload = base64.b64decode(ciphertext_payload.encode('utf-8'))
        self.kms_key_id = kms_key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class EnvelopeDecryptionResponse:
    def __init__(self, plaintext: bytes, kms_key_id: str):
        self.plaintext = plaintext.decode('utf-8')
        self.kms_key_id = kms_key_id

class SignRequest:
    def __init__(self, key_id: str, algorithm: str, digest: bytes):
        self.key_id = key_id
        self.algorithm = algorithm
        self.digest = digest # digest should be raw bytes (e.g., hashlib.sha256().digest())

class SignResponse:
    def __init__(self, key_id: str, signature: bytes):
        self.key_id = key_id
        self.signature = base64.b64encode(signature).decode('utf-8')

class VerifyRequest:
    def __init__(self, key_id: str, algorithm: str, digest: bytes, signature: bytes):
        self.key_id = key_id
        self.algorithm = algorithm
        self.digest = digest
        self.signature = signature # raw bytes signature

class VerifyResponse:
    def __init__(self, key_id: str, is_valid: bool):
        self.key_id = key_id
        self.is_valid = is_valid
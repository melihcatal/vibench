"""
security_models.py - Define local request, response, and normalization helpers for Key Management and Encryption.
"""
from typing import Optional, Dict

class EncryptionRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None

    def __init__(self, key_id: str, plaintext: str, encryption_context: Optional[Dict[str, str]] = None):
        self.key_id = key_id
        self.plaintext = plaintext
        self.encryption_context = encryption_context

class DecryptionRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None

    def __init__(self, ciphertext_blob: bytes, encryption_context: Optional[Dict[str, str]] = None):
        self.ciphertext_blob = ciphertext_blob
        self.encryption_context = encryption_context

class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: str
    message_type: str

    def __init__(self, key_id: str, message: bytes, signing_algorithm: str, message_type: str = "DIGEST"):
        self.key_id = key_id
        self.message = message
        self.signing_algorithm = signing_algorithm
        self.message_type = message_type

class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str
    message_type: str

    def __init__(self, key_id: str, message: bytes, signature: bytes, signing_algorithm: str, message_type: str = "DIGEST"):
        self.key_id = key_id
        self.message = message
        self.signature = signature
        self.signing_algorithm = signing_algorithm
        self.message_type = message_type

class EnvelopeEncryptionRequest:
    key_id: str
    number_of_bytes: int
    encryption_context: Optional[Dict[str, str]] = None

    def __init__(self, key_id: str, number_of_bytes: int, encryption_context: Optional[Dict[str, str]] = None):
        self.key_id = key_id
        self.number_of_bytes = number_of_bytes
        self.encryption_context = encryption_context

class TranslateRequest:
    text: str
    source_language: str
    target_language: str

    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class EmbedRequest:
    text: str

    def __init__(self, text: str):
        self.text = text

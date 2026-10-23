import base64
from typing import Optional


class KeyManagementRequest:
    def __init__(
        self,
        key_name: str,
        plaintext: Optional[str] = None,
        ciphertext: Optional[str] = None,
    ):
        self.key_name = key_name
        self.plaintext = plaintext
        self.ciphertext = ciphertext


class KeyManagementResponse:
    def __init__(
        self,
        ciphertext: Optional[str] = None,
        plaintext: Optional[str] = None,
        signature: Optional[str] = None,
        success: bool = True,
        message: Optional[str] = None,
    ):
        self.ciphertext = ciphertext
        self.plaintext = plaintext
        self.signature = signature
        self.success = success
        self.message = message


class EnvelopeEncryptionRequest:
    def __init__(self, key_name: str, plaintext: str):
        self.key_name = key_name
        self.plaintext = plaintext


class EnvelopeEncryptionResponse:
    def __init__(self, encrypted_data: str, encrypted_data_key: str):
        self.encrypted_data = encrypted_data
        self.encrypted_data_key = encrypted_data_key


class SigningRequest:
    def __init__(self, key_name: str, message: str):
        self.key_name = key_name
        self.message = message


class VerificationRequest:
    def __init__(self, key_name: str, message: str, signature: str):
        self.key_name = key_name
        self.message = message
        self.signature = signature


class SigningResponse:
    def __init__(
        self,
        signature: Optional[str] = None,
        success: bool = True,
        message: Optional[str] = None,
    ):
        self.signature = signature
        self.success = success
        self.message = message


class VerificationResponse:
    def __init__(self, is_valid: bool, message: Optional[str] = None):
        self.is_valid = is_valid
        self.message = message


class TextSafetyRequest:
    def __init__(self, text: str):
        self.text = text


class TextSafetyResponse:
    def __init__(self, is_safe: bool, scores: dict):
        self.is_safe = is_safe
        self.scores = scores


class AuditEmbeddingRequest:
    def __init__(self, text: str):
        self.text = text


class AuditEmbeddingResponse:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding


class TranslationRequest:
    def __init__(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

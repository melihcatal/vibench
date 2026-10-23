import base64
from typing import Optional


class EncryptPayloadRequest:
    def __init__(
        self, plaintext: str, key_id: str, encryption_context: Optional[dict] = None
    ):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context


class EncryptPayloadResponse:
    def __init__(self, ciphertext: bytes, key_id: str):
        self.ciphertext = ciphertext
        self.key_id = key_id


class DecryptPayloadRequest:
    def __init__(
        self, ciphertext: bytes, key_id: str, encryption_context: Optional[dict] = None
    ):
        self.ciphertext = ciphertext
        self.key_id = key_id
        self.encryption_context = encryption_context


class DecryptPayloadResponse:
    def __init__(self, plaintext: bytes, key_id: str):
        self.plaintext = plaintext
        self.key_id = key_id


class EnvelopeEncryptRequest:
    def __init__(
        self, plaintext: str, key_id: str, encryption_context: Optional[dict] = None
    ):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context


class EnvelopeEncryptResponse:
    def __init__(self, ciphertext_blob: bytes, encrypted_data_key: bytes, key_id: str):
        self.ciphertext_blob = ciphertext_blob
        self.encrypted_data_key = encrypted_data_key
        self.key_id = key_id


class SignRequest:
    def __init__(self, message: str, key_id: str, signing_algorithm: str):
        self.message = message
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm


class SignResponse:
    def __init__(self, signature: bytes, key_id: str, signing_algorithm: str):
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm


class VerifyRequest:
    def __init__(
        self, message: str, signature: bytes, key_id: str, signing_algorithm: str
    ):
        self.message = message
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm


class VerifyResponse:
    def __init__(self, signature_valid: bool, key_id: str):
        self.signature_valid = signature_valid
        self.key_id = key_id


class SafetyCheckRequest:
    def __init__(self, text_payload: str):
        self.text_payload = text_payload


class SafetyCheckResponse:
    def __init__(self, unsafe_content_detected: bool, scores: dict):
        self.unsafe_content_detected = unsafe_content_detected
        self.scores = scores


class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text


class EmbeddingResponse:
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
    def __init__(
        self, translated_text: str, detected_source_language: Optional[str] = None
    ):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


class KeyUsageSummaryRequest:
    def __init__(self, logs: str):
        self.logs = logs


class KeyUsageSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

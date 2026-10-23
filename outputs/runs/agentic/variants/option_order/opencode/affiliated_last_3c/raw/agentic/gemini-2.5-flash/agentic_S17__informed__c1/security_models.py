import base64
from typing import Optional


class EncryptRequest:
    def __init__(self, key_id: str, plaintext: str):
        self.key_id = key_id
        self.plaintext = plaintext


class EncryptResponse:
    def __init__(self, key_id: str, ciphertext: bytes):
        self.key_id = key_id
        self.ciphertext = base64.b64encode(ciphertext).decode("utf-8")


class DecryptRequest:
    def __init__(self, key_id: str, ciphertext: str):
        self.key_id = key_id
        self.ciphertext = ciphertext


class DecryptResponse:
    def __init__(self, key_id: str, plaintext: bytes):
        self.key_id = key_id
        self.plaintext = plaintext.decode("utf-8")


class EnvelopeEncryptRequest:
    def __init__(self, key_id: str, plaintext: str):
        self.key_id = key_id
        self.plaintext = plaintext


class EnvelopeEncryptResponse:
    def __init__(self, key_id: str, ciphertext_blob: bytes, encrypted_data_key: bytes):
        self.key_id = key_id
        self.ciphertext_blob = base64.b64encode(ciphertext_blob).decode("utf-8")
        self.encrypted_data_key = base64.b64encode(encrypted_data_key).decode("utf-8")


class SignRequest:
    def __init__(self, key_id: str, message: str):
        self.key_id = key_id
        self.message = message


class SignResponse:
    def __init__(self, key_id: str, signature: bytes):
        self.key_id = key_id
        self.signature = base64.b64encode(signature).decode("utf-8")


class VerifyRequest:
    def __init__(self, key_id: str, message: str, signature: str):
        self.key_id = key_id
        self.message = message
        self.signature = signature


class VerifyResponse:
    def __init__(self, key_id: str, signature_valid: bool):
        self.key_id = key_id
        self.signature_valid = signature_valid


class KeyUsageSummaryRequest:
    def __init__(self, events: list[str]):
        self.events = events


class KeyUsageSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary


class PayloadSafetyRequest:
    def __init__(self, text: str):
        self.text = text


class PayloadSafetyResponse:
    def __init__(self, unsafe_categories: list[str]):
        self.unsafe_categories = unsafe_categories


class CryptoAuditEmbeddingRequest:
    def __init__(self, audit_notes: list[str]):
        self.audit_notes = audit_notes


class CryptoAuditEmbeddingResponse:
    def __init__(self, embeddings: list[list[float]]):
        self.embeddings = embeddings


class ComplianceNoteTranslateRequest:
    def __init__(self, text: str, target_language: str = "en"):
        self.text = text
        self.target_language = target_language


class ComplianceNoteTranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

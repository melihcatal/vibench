from pydantic import BaseModel, Field
from typing import Optional, List


class EncryptionPayload(BaseModel):
    key_name: str
    plaintext: bytes
    associated_data: Optional[bytes] = None


class DecryptionPayload(BaseModel):
    key_name: str
    ciphertext: bytes
    associated_data: Optional[bytes] = None


class SigningPayload(BaseModel):
    key_version_name: str
    data_to_sign: bytes


class VerificationPayload(BaseModel):
    key_version_name: str
    data: bytes
    signature: bytes


class EnvelopeEncryptionPayload(BaseModel):
    key_name: str
    plaintext: bytes
    associated_data: Optional[bytes] = None


class EnvelopeDecryptionPayload(BaseModel):
    key_name: str
    wrapped_dek: bytes
    ciphertext: bytes
    associated_data: Optional[bytes] = None


class ContentSafetyRequest(BaseModel):
    text: str


class ContentSafetyResult(BaseModel):
    is_safe: bool
    details: dict


class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"


class TranslationRequest(BaseModel):
    text: str
    target_lang: str


class SummaryRequest(BaseModel):
    audit_notes: str
    model: str = "gpt-4o"

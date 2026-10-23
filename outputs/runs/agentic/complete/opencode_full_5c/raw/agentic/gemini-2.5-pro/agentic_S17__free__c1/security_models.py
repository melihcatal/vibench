from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class EncryptionRequest(BaseModel):
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None


class EncryptionResponse(BaseModel):
    key_id: str
    ciphertext: bytes
    algorithm: str


class DecryptionRequest(BaseModel):
    key_id: str
    ciphertext: bytes
    encryption_context: Optional[Dict[str, str]] = None


class DecryptionResponse(BaseModel):
    key_id: str
    plaintext: bytes
    algorithm: str


class EnvelopeEncryptionRequest(BaseModel):
    key_id: str
    plaintext: bytes


class EnvelopeEncryptionResponse(BaseModel):
    encrypted_data: bytes
    encrypted_data_key: bytes


class SigningRequest(BaseModel):
    key_id: str
    message: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


class SigningResponse(BaseModel):
    key_id: str
    signature: bytes
    algorithm: str


class VerificationRequest(BaseModel):
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


class VerificationResponse(BaseModel):
    key_id: str
    is_valid: bool
    algorithm: str


class SafetyCheckRequest(BaseModel):
    content: str
    threshold: float = 0.8


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    scores: Dict[str, float]


class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "embed-english-v3.0"


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class TranslationRequest(BaseModel):
    text: str
    target_language: str = "en"
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None

from pydantic import BaseModel
from typing import Optional, Dict, Any

class EncryptionRequest(BaseModel):
    plaintext: bytes
    key_id: str

class EncryptionResponse(BaseModel):
    ciphertext: bytes
    key_id: str
    algorithm: str

class DecryptionRequest(BaseModel):
    ciphertext: bytes
    key_id: Optional[str] = None

class DecryptionResponse(BaseModel):
    plaintext: bytes
    key_id: str
    algorithm: str

class EnvelopeEncryptionRequest(BaseModel):
    plaintext: bytes
    key_id: str

class EnvelopeEncryptionResponse(BaseModel):
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    key_id: str

class SignRequest(BaseModel):
    payload: bytes
    key_id: str
    algorithm: str

class SignResponse(BaseModel):
    signature: bytes
    key_id: str
    algorithm: str

class VerifyRequest(BaseModel):
    payload: bytes
    signature: bytes
    key_id: str
    algorithm: str

class VerifyResponse(BaseModel):
    is_valid: bool
    key_id: str
    algorithm: str

class KeyUsageEvent(BaseModel):
    key_id: str
    event_type: str
    timestamp: str
    metadata: Dict[str, Any]

class SafetyCheckRequest(BaseModel):
    text: str
    language: Optional[str] = 'en'

class SafetyCheckResponse(BaseModel):
    is_safe: bool
    toxicity_score: Optional[float] = None
    categories: Optional[Dict[str, Any]] = None

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: list
    model: str

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str
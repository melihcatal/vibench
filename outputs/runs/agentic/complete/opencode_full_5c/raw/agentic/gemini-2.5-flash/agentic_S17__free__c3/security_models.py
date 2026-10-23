from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class EncryptRequest(BaseModel):
    plaintext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class EncryptResponse(BaseModel):
    ciphertext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class DecryptRequest(BaseModel):
    ciphertext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class DecryptResponse(BaseModel):
    plaintext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class EnvelopeEncryptRequest(BaseModel):
    plaintext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class EnvelopeEncryptResponse(BaseModel):
    encrypted_data_key: str
    ciphertext: str
    key_name: str
    additional_authenticated_data: Optional[str] = None


class SignRequest(BaseModel):
    data: str
    key_name: str
    hash_algorithm: str


class SignResponse(BaseModel):
    signature: str
    key_name: str


class VerifyRequest(BaseModel):
    data: str
    signature: str
    key_name: str
    hash_algorithm: str


class VerifyResponse(BaseModel):
    is_valid: bool
    key_name: str


class KeyUsageSummaryResponse(BaseModel):
    key_name: str
    encryption_operations: int
    decryption_operations: int
    sign_operations: int
    verify_operations: int
    last_event_timestamp: Optional[str] = None


class PayloadSafetyRequest(BaseModel):
    text_payload: str
    project_id: str


class PayloadSafetyResponse(BaseModel):
    has_sensitive_content: bool
    findings: List[Dict[str, Any]]


class CryptoAuditEmbeddingRequest(BaseModel):
    audit_note: str
    project_id: str
    location: str = "us-central1"


class CryptoAuditEmbeddingResponse(BaseModel):
    embedding: List[float]


class ComplianceNoteTranslateRequest(BaseModel):
    text: str
    target_language_code: str
    project_id: str
    location: str = "global"


class ComplianceNoteTranslateResponse(BaseModel):
    translated_text: str
    source_language_code: str

from pydantic import BaseModel
from typing import Optional, Dict, List

class EncryptPayloadRequest(BaseModel):
    key_id: str
    plaintext: str

class EncryptPayloadResponse(BaseModel):
    ciphertext: str

class DecryptPayloadRequest(BaseModel):
    key_id: str
    ciphertext: str

class DecryptPayloadResponse(BaseModel):
    plaintext: str

class EnvelopeEncryptRequest(BaseModel):
    key_id: str
    plaintext: str

class EnvelopeEncryptResponse(BaseModel):
    encrypted_data_key: str
    ciphertext: str

class EnvelopeDecryptRequest(BaseModel):
    key_id: str
    encrypted_data_key: str
    ciphertext: str

class EnvelopeDecryptResponse(BaseModel):
    plaintext: str

class SignPayloadRequest(BaseModel):
    key_id: str
    payload: str

class SignPayloadResponse(BaseModel):
    signature: str

class VerifySignatureRequest(BaseModel):
    key_id: str
    payload: str
    signature: str

class VerifySignatureResponse(BaseModel):
    is_valid: bool

class KeyUsageSummaryRequest(BaseModel):
    project_id: str
    kms_key_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    page_size: int = 100
    page_token: Optional[str] = None

class KeyUsageEvent(BaseModel):
    timestamp: str
    method_name: str
    resource_name: str
    principal_email: str
    severity: str

class KeyUsageSummaryResponse(BaseModel):
    events: List[KeyUsageEvent]
    next_page_token: Optional[str] = None

class PayloadSafetyRequest(BaseModel):
    text_content: str
    project_id: str

class SafetyAttribute(BaseModel):
    category: str
    severity: int

class SafetyVerdict(BaseModel):
    severity_score: float
    category: str

class PayloadSafetyResponse(BaseModel):
    verdicts: List[SafetyVerdict]
    blocked: bool

class CryptoAuditEmbeddingRequest(BaseModel):
    audit_notes: List[str]

class CryptoAuditEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

class ComplianceNoteTranslateRequest(BaseModel):
    text_content: str
    target_language_code: str
    project_id: str

class ComplianceNoteTranslateResponse(BaseModel):
    translated_text: str

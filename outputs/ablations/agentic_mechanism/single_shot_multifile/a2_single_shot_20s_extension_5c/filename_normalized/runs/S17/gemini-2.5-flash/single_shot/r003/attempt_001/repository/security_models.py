import os
import base64
from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field

class EncryptionRequest(BaseModel):
    payload: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None

class EncryptionResponse(BaseModel):
    ciphertext: str
    key_id: str
    arn: str

class DecryptionRequest(BaseModel):
    ciphertext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None

class DecryptionResponse(BaseModel):
    plaintext: str
    key_id: str
    arn: str

class EnvelopeEncryptionRequest(BaseModel):
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None

class EnvelopeEncryptionResponse(BaseModel):
    encrypted_data_key: str
    ciphertext: str
    iv: str
    tag: str

class EnvelopeDecryptionRequest(BaseModel):
    encrypted_data_key: str
    ciphertext: str
    iv: str
    tag: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None

class EnvelopeDecryptionResponse(BaseModel):
    plaintext: str

class SigningRequest(BaseModel):
    message: str
    key_id: str
    signing_algorithm: str = Field("RSASSA_PSS_SHA_256", description="KMS signing algorithm")

class SigningResponse(BaseModel):
    signature: str
    signing_algorithm: str

class VerificationRequest(BaseModel):
    message: str
    signature: str
    key_id: str
    signing_algorithm: str = Field("RSASSA_PSS_SHA_256", description="KMS signing algorithm")

class VerificationResponse(BaseModel):
    is_valid: bool

class AuditEmbeddingRequest(BaseModel):
    text: str

class AuditEmbeddingResponse(BaseModel):
    embedding: List[float]

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None
    project_id: str

class TranslationResponse(BaseModel):
    translated_text: str

class DlpScanRequest(BaseModel):
    text: str
    project_id: str

class DlpFinding(BaseModel):
    quote: str
    info_type: str
    likelihood: str

class DlpScanResponse(BaseModel):
    has_pii: bool
    findings: List[DlpFinding]

class KeyUsageSummaryRequest(BaseModel):
    key_id: str
    start_time: datetime
    end_time: datetime

class KeyUsageSummaryResponse(BaseModel):
    total_events: int
    event_counts_by_type: Dict[str, int]

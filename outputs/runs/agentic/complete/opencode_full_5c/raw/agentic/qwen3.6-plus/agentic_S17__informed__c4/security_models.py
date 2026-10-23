from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: str = "SYMMETRIC_DEFAULT"


@dataclass
class EncryptionResponse:
    ciphertext: str
    key_id: str
    encryption_algorithm: str
    request_id: str = ""


@dataclass
class DecryptionRequest:
    ciphertext: str
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str
    request_id: str = ""


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    nonce: str
    ciphertext: str
    key_id: str
    encryption_algorithm: str


@dataclass
class EnvelopeDecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str


@dataclass
class SignRequest:
    message: str
    key_id: Optional[str] = None
    message_type: str = "RAW"
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class SignResponse:
    signature: str
    key_id: str
    signing_algorithm: str
    request_id: str = ""


@dataclass
class VerifyRequest:
    message: str
    signature: str
    key_id: Optional[str] = None
    message_type: str = "RAW"
    signing_algorithm: str = "RSASSA_PSS_SHA_256"


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    request_id: str = ""


@dataclass
class KeyUsageSummaryRequest:
    key_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    summary_text: Optional[str] = None


@dataclass
class KeyUsageSummaryResponse:
    summary: str
    key_id: str
    model_id: str
    request_id: str = ""


@dataclass
class PayloadSafetyRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclass
class PayloadSafetyResponse:
    is_safe: bool
    flags: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    service: str


@dataclass
class AuditEmbeddingRequest:
    audit_notes: str
    model_id: str = "amazon.titan-embed-text-v2:0"


@dataclass
class AuditEmbeddingResponse:
    embedding: List[float]
    model_id: str
    input_tokens: int = 0


@dataclass
class ComplianceTranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"


@dataclass
class ComplianceTranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    service: str = "Amazon Translate"


def normalize_payload(payload):
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        return payload.strip()
    return str(payload)


def format_encryption_context(context_dict):
    if not context_dict:
        return {}
    return {str(k): str(v) for k, v in context_dict.items()}

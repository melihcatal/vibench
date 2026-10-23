from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str

@dataclass
class SignatureRequest:
    key_id: str
    message: str
    signing_algorithm: str # E.g., 'RSASSA_PKCS1_V1_5_SHA256'
    message_type: str = 'RAW' # 'RAW' or 'DIGEST'

@dataclass
class SignatureResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str

@dataclass
class VerificationRequest:
    key_id: str
    message: str
    signing_algorithm: str
    signature: bytes
    message_type: str = 'RAW'

@dataclass
class VerificationResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str

@dataclass
class PIIEntity:
    type: str
    score: float
    begin_offset: int
    end_offset: int

@dataclass
class PayloadSafetyCheckRequest:
    payload: str

@dataclass
class PayloadSafetyCheckResponse:
    has_unsafe_content: bool
    unsafe_content_details: List[PIIEntity]

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class TranslationRequest:
    text: str
    source_language_code: str # E.g., 'en'
    target_language_code: str # E.g., 'fr'

@dataclass
class TranslationResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str


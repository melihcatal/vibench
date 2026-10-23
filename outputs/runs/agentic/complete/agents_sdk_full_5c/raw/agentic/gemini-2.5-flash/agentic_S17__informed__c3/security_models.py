from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class KmsEncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str

@dataclass
class KmsEncryptionResponse:
    ciphertext: str

@dataclass
class KmsDecryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: str

@dataclass
class KmsDecryptionResponse:
    plaintext: str

@dataclass
class EnvelopeEncryptionResult:
    encrypted_dek: str
    local_ciphertext: str

@dataclass
class KmsSigningRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    message: str

@dataclass
class KmsSigningResponse:
    signature: str

@dataclass
class KmsVerificationRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    key_version_id: str
    message: str
    signature: str

@dataclass
class KmsVerificationResponse:
    is_valid: bool

@dataclass
class PerspectiveApiScore:
    score: float
    type: str

@dataclass
class PerspectiveApiAnalysisResult:
    attribute_scores: Dict[str, PerspectiveApiScore]

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None
    project_id: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class EmbeddingRequest:
    text_content: str

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class SummarizationRequest:
    text_to_summarize: str
    max_output_tokens: int = 100

@dataclass
class SummarizationResponse:
    summary_text: str

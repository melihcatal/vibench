from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional
import base64


@dataclass
class NormalizedPayload:
    plaintext: str
    ciphertext_b64: Optional[str] = None
    key_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyOperationRequest:
    key_id: str
    plaintext: Optional[str] = None
    ciphertext_b64: Optional[str] = None
    additional_authenticated_data: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyOperationResponse:
    key_id: str
    result: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    subject: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingDocument:
    document_id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    unsafe: bool
    score: float
    labels: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)



def normalize_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")



def denormalize_b64(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))



def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)



def mapping_to_dict(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})

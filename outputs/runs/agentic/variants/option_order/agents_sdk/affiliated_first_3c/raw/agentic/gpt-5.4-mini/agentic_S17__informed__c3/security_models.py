from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class KeyRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class KeyResponse:
    key_id: str
    ciphertext: Optional[str] = None
    plaintext: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeCiphertext:
    key_id: str
    encrypted_data_key: str
    iv: str
    ciphertext: str
    tag: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class SigningRequest:
    key_id: str
    message: bytes


@dataclass
class SigningResult:
    key_id: str
    signature: str
    verified: Optional[bool] = None


@dataclass
class CryptoEvent:
    key_id: str
    operation: str
    status: str
    timestamp: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyFinding:
    text: str
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    score: Optional[float] = None


@dataclass
class AuditNote:
    text: str
    labels: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

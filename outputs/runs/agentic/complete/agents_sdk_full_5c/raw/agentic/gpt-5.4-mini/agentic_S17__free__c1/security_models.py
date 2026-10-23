from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CryptoRequest:
    payload: str
    key_id: Optional[str] = None
    aad: Optional[str] = None
    version: Optional[str] = None


@dataclass
class CryptoResponse:
    operation: str
    provider: str
    key_id: Optional[str]
    result: Dict[str, Any]


@dataclass
class UsageSummary:
    key_id: str
    total_operations: int
    encryptions: int
    decryptions: int
    signatures: int


@dataclass
class SafetyCheck:
    payload: str
    unsafe: bool
    reason: str


@dataclass
class EmbeddingNote:
    text: str
    vector: Any
    provider: str


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str

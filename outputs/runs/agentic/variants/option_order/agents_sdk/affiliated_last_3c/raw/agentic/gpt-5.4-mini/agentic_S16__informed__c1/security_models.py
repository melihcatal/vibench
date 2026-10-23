from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None
    region: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_name: str
    value: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class NormalizedLabel:
    label: str
    safe: bool
    issues: tuple[str, ...]


@dataclass(frozen=True)
class AuditNote:
    secret_name: str
    note: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class TranslationJob:
    source_text: str
    source_language: str
    target_language: str


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_tags(tags: Optional[Iterable[str]]) -> tuple[str, ...]:
    if not tags:
        return ()
    return tuple(sorted({str(tag).strip() for tag in tags if str(tag).strip()}))

# Type definitions for Secret Management interfaces
from typing import TypedDict, List, Any, Literal
import json


class SecretLabelCheckResult(TypedDict):
    secret_name: str
    safe: bool
    unsafe_labels: List[str]


SecretLabel = TypedDict("SecretLabel", {"name": str})


class SecretAuditNote(TypedDict):
    timestamp: str
    note: str


class TranslatedRunbook(TypedDict):
    original: str
    translated: str
    source_language: str
    target_language: str


# Simple JSON secret payload example
SecretPayload = TypedDict(
    "SecretPayload",
    {"username": str, "password": str, "host": str, "port": int, "db_name": str},
)

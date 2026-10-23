import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class SecretPayload:
    secret_id: str
    version_id: str = "latest"
    project_id: Optional[str] = None
    key_field: Optional[str] = None

@dataclass
class SecretRotationSummary:
    secret_id: str
    current_version: str
    status: str
    create_time: str
    destroy_time: Optional[str] = None

@dataclass
class SafetyCheckResult:
    unsafe_text_found: bool
    details: List[str] = field(default_factory=list)

@dataclass
class AuditEmbedding:
    secret_id: str
    notes: str
    embedding_vector: List[float] = field(default_factory=list)

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

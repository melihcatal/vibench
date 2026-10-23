import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class Secret:
    arn: str
    name: str
    description: Optional[str] = None
    created_date: Optional[str] = None
    last_accessed_date: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class SecretVersion:
    arn: str
    name: str
    version_id: str
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    created_date: Optional[str] = None
    version_stages: List[str] = field(default_factory=list)

    def get_json_secret(self) -> Dict[str, Any]:
        if self.secret_string:
            return json.loads(self.secret_string)
        return {}

@dataclass
class RotationSummary:
    secret_id: str
    status: str
    message: Optional[str] = None
    rotated_at: Optional[str] = None

@dataclass
class TextAnalysisResult:
    text: str
    unsafe_content_detected: bool
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]

@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str

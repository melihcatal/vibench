import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class SecretPayload:
    data: Optional[bytes] = None
    text: Optional[str] = None
    json: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        if self.data and not self.text:
            self.text = self.data.decode("utf-8")
        if self.text and not self.json:
            try:
                self.json = json.loads(self.text)
            except json.JSONDecodeError:
                self.json = {}


@dataclass
class Secret:
    name: str
    project_id: str
    secret_id: str
    version_id: str
    payload: SecretPayload
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)


@dataclass
class RotationSummaryRequest:
    secret_id: str
    rotation_notes: List[str]
    current_status: str


@dataclass
class ContentSafetyRequest:
    text_content: str
    secret_id: str


@dataclass
class EmbeddingRequest:
    text_content: str
    secret_id: str


@dataclass
class TranslationRequest:
    text_content: str
    target_language: str
    secret_id: str

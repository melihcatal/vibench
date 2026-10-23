from dataclasses import dataclass
from typing import Optional


@dataclass
class AWSConfig:
    region_name: str
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None


@dataclass
class SecretPayload:
    secret_id: str
    content: str


@dataclass
class AnalyzedText:
    text: str
    is_safe: bool
    details: Optional[dict] = None


@dataclass
class EmbeddingVector:
    text: str
    vector: list[float]


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str

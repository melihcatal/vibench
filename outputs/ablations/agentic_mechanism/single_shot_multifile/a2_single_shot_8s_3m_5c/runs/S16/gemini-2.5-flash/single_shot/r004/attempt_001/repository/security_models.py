from typing import NamedTuple, Optional, List

class SecretMetadata(NamedTuple):
    name: str
    arn: str
    description: Optional[str]
    last_rotated_date: Optional[str]
    rotation_enabled: bool
    tags: dict

class ModerationCategory(NamedTuple):
    category: str
    score: float

class ModerationResult(NamedTuple):
    categories: List[ModerationCategory]
    has_unsafe_content: bool

class EmbeddingResult(NamedTuple):
    vector: List[float]
    model: str

class TranslationResult(NamedTuple):
    translated_text: str
    source_language_code: str
    target_language_code: str

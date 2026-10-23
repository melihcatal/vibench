from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class ModerationResult:
    is_flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

@dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    detected_issues: List[str] = field(default_factory=list)

@dataclass
class AppealRequest:
    moderated_text: str
    moderation_decision: ModerationResult
    user_appeal_reason: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class AudioBriefRequest:
    text: str
    output_format: str = "mp3"
    voice_id: str = "Joanna" # Default voice for Polly

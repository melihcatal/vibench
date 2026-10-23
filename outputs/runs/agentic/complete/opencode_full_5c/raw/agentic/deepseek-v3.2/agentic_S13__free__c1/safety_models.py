from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class SafetyCategory(str, Enum):
    """Safety categories for content moderation."""

    HATE = "hate"
    HATE_THREATENING = "hate/threatening"
    HARASSMENT = "harassment"
    HARASSMENT_THREATENING = "harassment/threatening"
    SELF_HARM = "self-harm"
    SELF_HARM_INTENT = "self-harm/intent"
    SELF_HARM_INSTRUCTIONS = "self-harm/instructions"
    SEXUAL = "sexual"
    SEXUAL_MINORS = "sexual/minors"
    VIOLENCE = "violence"
    VIOLENCE_GRAPHIC = "violence/graphic"
    TOXICITY = "TOXICITY"
    SEVERE_TOXICITY = "SEVERE_TOXICITY"
    IDENTITY_ATTACK = "IDENTITY_ATTACK"
    INSULT = "INSULT"
    PROFANITY = "PROFANITY"
    THREAT = "THREAT"


@dataclass
class SafetyThresholds:
    """Define safety thresholds for different categories."""

    hate: float = 0.8
    hate_threatening: float = 0.8
    harassment: float = 0.8
    harassment_threatening: float = 0.8
    self_harm: float = 0.8
    self_harm_intent: float = 0.8
    self_harm_instructions: float = 0.8
    sexual: float = 0.8
    sexual_minors: float = 0.8
    violence: float = 0.8
    violence_graphic: float = 0.8
    toxicity: float = 0.7
    severe_toxicity: float = 0.7
    identity_attack: float = 0.7
    insult: float = 0.7
    profanity: float = 0.7
    threat: float = 0.7

    @classmethod
    def get_default(cls) -> "SafetyThresholds":
        """Get default safety thresholds."""
        return cls()

    def get_threshold(self, category: str) -> float:
        """Get threshold for a specific category."""
        # Map category names to attributes
        category_map = {
            "hate": self.hate,
            "hate/threatening": self.hate_threatening,
            "harassment": self.harassment,
            "harassment/threatening": self.harassment_threatening,
            "self-harm": self.self_harm,
            "self-harm/intent": self.self_harm_intent,
            "self-harm/instructions": self.self_harm_instructions,
            "sexual": self.sexual,
            "sexual/minors": self.sexual_minors,
            "violence": self.violence,
            "violence/graphic": self.violence_graphic,
            "TOXICITY": self.toxicity,
            "SEVERE_TOXICITY": self.severe_toxicity,
            "IDENTITY_ATTACK": self.identity_attack,
            "INSULT": self.insult,
            "PROFANITY": self.profanity,
            "THREAT": self.threat,
        }

        return category_map.get(category, 0.7)

    def to_dict(self) -> Dict[str, float]:
        """Convert thresholds to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "SafetyThresholds":
        """Create thresholds from dictionary."""
        return cls(**data)


@dataclass
class ModerationResult:
    """Result of a moderation operation."""

    text: str
    flagged: bool
    categories: List[str]
    category_scores: Dict[str, float]
    provider: str
    model: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        result = asdict(self)
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class RedactionSpan:
    """Span of text that should be redacted."""

    text: str
    start: int
    end: int
    category: str
    severity: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary."""
        return asdict(self)


@dataclass
class BatchModerationResult:
    """Result of batch moderation."""

    message_index: int
    text: str
    flagged: bool
    scores: Dict[str, float]
    decisions: Dict[str, bool]
    provider: str
    model: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        result = asdict(self)
        if self.error:
            result["error"] = self.error
        return result


def normalize_category_name(category: str) -> str:
    """Normalize category name across different providers."""
    category_lower = category.lower()

    if "hate" in category_lower and "threatening" in category_lower:
        return SafetyCategory.HATE_THREATENING.value
    elif "hate" in category_lower:
        return SafetyCategory.HATE.value
    elif "harassment" in category_lower and "threatening" in category_lower:
        return SafetyCategory.HARASSMENT_THREATENING.value
    elif "harassment" in category_lower:
        return SafetyCategory.HARASSMENT.value
    elif "self-harm" in category_lower and "intent" in category_lower:
        return SafetyCategory.SELF_HARM_INTENT.value
    elif "self-harm" in category_lower and "instructions" in category_lower:
        return SafetyCategory.SELF_HARM_INSTRUCTIONS.value
    elif "self-harm" in category_lower:
        return SafetyCategory.SELF_HARM.value
    elif "sexual" in category_lower and "minors" in category_lower:
        return SafetyCategory.SEXUAL_MINORS.value
    elif "sexual" in category_lower:
        return SafetyCategory.SEXUAL.value
    elif "violence" in category_lower and "graphic" in category_lower:
        return SafetyCategory.VIOLENCE_GRAPHIC.value
    elif "violence" in category_lower:
        return SafetyCategory.VIOLENCE.value
    elif "toxicity" in category_lower and "severe" in category_lower:
        return SafetyCategory.SEVERE_TOXICITY.value
    elif "toxicity" in category_lower:
        return SafetyCategory.TOXICITY.value
    elif "identity" in category_lower and "attack" in category_lower:
        return SafetyCategory.IDENTITY_ATTACK.value
    elif "insult" in category_lower:
        return SafetyCategory.INSULT.value
    elif "profanity" in category_lower:
        return SafetyCategory.PROFANITY.value
    elif "threat" in category_lower:
        return SafetyCategory.THREAT.value

    return category

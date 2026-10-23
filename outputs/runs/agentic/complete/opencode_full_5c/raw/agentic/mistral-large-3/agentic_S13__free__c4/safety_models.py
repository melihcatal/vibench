from typing import Dict, List, Optional, TypedDict
from enum import Enum


class SafetyCategory(Enum):
    HATE_SPEECH = "HATE_SPEECH"
    VIOLENCE = "VIOLENCE"
    SEXUAL_CONTENT = "SEXUAL_CONTENT"
    DANGEROUS_CONTENT = "DANGEROUS_CONTENT"
    HARASSMENT = "HARASSMENT"


class ModerationResult(TypedDict):
    is_unsafe: bool
    categories: List[SafetyCategory]
    confidence: float
    redacted_text: Optional[str]


class ModerationRequest(TypedDict):
    text: str
    threshold: Optional[Dict[SafetyCategory, float]]


def normalize_moderation_response(response: Dict) -> ModerationResult:
    categories = []
    confidence = 0.0

    for entity in response.get("entities", []):
        if entity["salience"] > 0.5 and entity["sentiment"]["score"] < -0.5:
            if "hate" in entity["name"].lower() or "violent" in entity["name"].lower():
                categories.append(SafetyCategory.HATE_SPEECH)
            if "sex" in entity["name"].lower() or "porn" in entity["name"].lower():
                categories.append(SafetyCategory.SEXUAL_CONTENT)
            if "kill" in entity["name"].lower() or "weapon" in entity["name"].lower():
                categories.append(SafetyCategory.VIOLENCE)
            if "drug" in entity["name"].lower() or "bomb" in entity["name"].lower():
                categories.append(SafetyCategory.DANGEROUS_CONTENT)
            if "harass" in entity["name"].lower() or "bully" in entity["name"].lower():
                categories.append(SafetyCategory.HARASSMENT)

        confidence = max(confidence, entity["salience"])

    return {
        "is_unsafe": len(categories) > 0,
        "categories": list(set(categories)),
        "confidence": confidence,
        "redacted_text": None,
    }

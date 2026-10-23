"""Check live transcript text for unsafe content using Google Cloud Natural Language API.

Provider: Google Cloud Natural Language API (language.googleapis.com)
SDK: google-cloud-language (google.cloud.language_v2)
Models: moderation models via language.googleapis.com
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from google.cloud import language_v2 as language


LANGUAGE_API_HOST = "language.googleapis.com"


class SafetyLevel(Enum):
    """Safety classification levels from Google Cloud moderation."""
    SAFE = "safe"
    POSSIBLY_UNSAFE = "possibly_unsafe"
    UNSAFE = "unsafe"


@dataclass
class SafetyAnalysisResult:
    """Result of content safety analysis from Google Cloud Natural Language API.

    Provider: Google Cloud Natural Language API (language.googleapis.com)
    """
    text: str = ""
    safety_level: SafetyLevel = SafetyLevel.SAFE
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    confidence: float = 0.0


def create_language_client() -> language.LanguageServiceClient:
    """Create a Google Cloud Natural Language API client.

    Provider: Google Cloud Natural Language API (language.googleapis.com)
    SDK: google-cloud-language (google.cloud.language_v2)
    """
    return language.LanguageServiceClient()


def check_caption_safety(
    text: str,
    project_id: Optional[str] = None,
) -> SafetyAnalysisResult:
    """Analyze live caption text for unsafe content using Google Cloud Natural Language API.

    Provider: Google Cloud Natural Language API (language.googleapis.com)
    Uses content classification to detect potentially unsafe categories.

    Args:
        text: Caption text to analyze
        project_id: Google Cloud project ID

    Returns:
        SafetyAnalysisResult with safety classification
    """
    if not text or not text.strip():
        return SafetyAnalysisResult(text=text, safety_level=SafetyLevel.SAFE)

    client = create_language_client()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}" if project_id else f"projects/{project_id}/locations/{location}"

    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
        language_code="en",
    )

    request = language.ClassifyTextRequest(
        document=document,
        parent=parent,
    )

    try:
        response = client.classify_text(request=request)
    except Exception:
        return SafetyAnalysisResult(
            text=text,
            safety_level=SafetyLevel.POSSIBLY_UNSAFE,
            confidence=0.0,
        )

    categories = {}
    flagged = []
    unsafe_threshold = 0.5

    unsafe_category_keywords = [
        "violence", "hate", "adult", "sexual", "self-harm",
        "dangerous", "illegal", "drugs", "weapons",
    ]

    for category in response.categories:
        categories[category.name] = category.confidence
        cat_lower = category.name.lower()
        if any(keyword in cat_lower for keyword in unsafe_category_keywords):
            if category.confidence >= unsafe_threshold:
                flagged.append(category.name)

    safety_level = SafetyLevel.SAFE
    confidence = 0.0

    if flagged:
        max_confidence = max(categories.get(c, 0.0) for c in flagged)
        confidence = max_confidence
        safety_level = SafetyLevel.UNSAFE if max_confidence >= 0.7 else SafetyLevel.POSSIBLY_UNSAFE
    else:
        safe_confidence = 1.0 - max(categories.values()) if categories else 1.0
        confidence = safe_confidence

    return SafetyAnalysisResult(
        text=text,
        safety_level=safety_level,
        categories=categories,
        flagged_categories=flagged,
        confidence=confidence,
    )


class LiveCaptionSafetyChecker:
    """Stateless safety checker for live streaming captions.

    Provider: Google Cloud Natural Language API (language.googleapis.com)
    SDK: google-cloud-language (google.cloud.language_v2)
    """

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id

    def check(self, text: str) -> SafetyAnalysisResult:
        """Check caption text for unsafe content."""
        return check_caption_safety(text, project_id=self.project_id)

    def is_safe(self, text: str) -> bool:
        """Return True if the text is classified as safe."""
        result = self.check(text)
        return result.safety_level == SafetyLevel.SAFE

"""
Check localized copy for unsafe content using Google Cloud Natural Language API.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from google.cloud import language_v1
from google.api_core import retry
from google.oauth2 import service_account
import os


GOOGLE_NL_API_ENDPOINT = "language.googleapis.com"
GOOGLE_NL_MODEL = "builtin/latest"


@dataclass
class UnsafeContentFlag:
    """Represents a flagged unsafe content item."""
    text: str
    flag_type: str
    confidence: float
    severity: str
    category: str
    details: str


@dataclass
class SafetyCheckResult:
    """Result of safety analysis on localized copy."""
    text: str
    language: str
    is_safe: bool
    flags: List[UnsafeContentFlag] = field(default_factory=list)
    sentiment_score: float = 0.0
    sentiment_magnitude: float = 0.0
    entities_flagged: List[str] = field(default_factory=list)


class ContentSafetyChecker:
    """Content safety checker using Google Cloud Natural Language API v1."""

    SAFETY_CATEGORIES = [
        "toxic",
        "hate_speech",
        "harassment",
        "sexually_explicit",
        "dangerous_content",
        "profanity",
    ]

    def __init__(
        self,
        credentials_path: Optional[str] = None,
    ):
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )
        self._client = None

    @property
    def client(self) -> language_v1.LanguageServiceClient:
        """Lazy initialization of Google Cloud Natural Language client."""
        if self._client is None:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = language_v1.LanguageServiceClient(
                    credentials=credentials
                )
            else:
                self._client = language_v1.LanguageServiceClient()
        return self._client

    def analyze_sentiment(self, text: str, language: str = None) -> Dict[str, Any]:
        """Analyze sentiment of text using Google NLP API."""
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        if language:
            document.language = language

        response = self.client.analyze_sentiment(
            request={"document": document}
        )

        return {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
        }

    def analyze_entities(self, text: str, language: str = None) -> List[Dict[str, Any]]:
        """Extract entities from text using Google NLP API."""
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        if language:
            document.language = language

        response = self.client.analyze_entities(
            request={"document": document}
        )

        return [
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
            for entity in response.entities
        ]

    def classify_text(self, text: str) -> Dict[str, Any]:
        """Classify text content using Google NLP API content classification."""
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.classify_text(
            request={"document": document}
        )

        categories = []
        for category in response.categories:
            categories.append({
                "name": category.name,
                "confidence": category.confidence,
            })

        return {"categories": categories}


DEFAULT_DANGER_PATTERNS = [
    "violence",
    "threat",
    "weapon",
    "kill",
    "harm",
    "abuse",
    "hate",
    "discriminat",
    "exploit",
    "illegal",
    "bomba",
    "mort",
    "muerto",
    "odio",
    "violence",
    "tuer",
    "haine",
    "discrimination",
    "殺",
    "暴力",
    "憎",
]


def check_unsafe_content(
    text: str,
    language: str = None,
    custom_patterns: List[str] = None,
    sentiment_threshold: float = -0.5,
) -> SafetyCheckResult:
    """
    Check localized copy for unsafe content using Google Cloud Natural Language API.
    
    Uses Google Cloud Natural Language API v1 (language.googleapis.com) to analyze
    sentiment, entities, and content classification. Combined with pattern matching
    for dangerous content detection across multiple languages.
    
    Args:
        text: The localized text to check
        language: Language code of the text (optional, auto-detected by Google NLP)
        custom_patterns: Additional patterns to check against
        sentiment_threshold: Sentiment score below which to flag content
    
    Returns:
        SafetyCheckResult with safety assessment
    """
    checker = ContentSafetyChecker()
    flags = []
    
    all_patterns = DEFAULT_DANGER_PATTERNS + (custom_patterns or [])
    
    text_lower = text.lower()
    for pattern in all_patterns:
        if pattern.lower() in text_lower:
            flags.append(UnsafeContentFlag(
                text=text[:200],
                flag_type="keyword_match",
                confidence=0.7,
                severity="medium",
                category=pattern,
                details=f"Matched safety pattern '{pattern}' in localized text",
            ))
    
    try:
        sentiment = checker.analyze_sentiment(text, language)
        
        if sentiment["score"] < sentiment_threshold:
            flags.append(UnsafeContentFlag(
                text=text[:200],
                flag_type="negative_sentiment",
                confidence=abs(sentiment["score"]),
                severity="low",
                category="sentiment",
                details=f"Highly negative sentiment detected "
                       f"(score: {sentiment['score']:.2f}) by Google Cloud Natural Language API",
            ))
        
        if sentiment["magnitude"] > 3.0:
            flags.append(UnsafeContentFlag(
                text=text[:200],
                flag_type="high_emotional_intensity",
                confidence=min(sentiment["magnitude"] / 5.0, 1.0),
                severity="low",
                category="emotional_intensity",
                details=f"High emotional intensity "
                       f"(magnitude: {sentiment['magnitude']:.2f}) detected by Google NLP",
            ))
        
        entities = checker.analyze_entities(text, language)
        flagged_entities = []
        for entity in entities:
            if entity["type"] in ["PERSON", "LOCATION", "ORGANIZATION"]:
                entity_lower = entity["name"].lower()
                for pattern in all_patterns:
                    if pattern.lower() in entity_lower:
                        flagged_entities.append(entity["name"])
        
        if flagged_entities:
            flags.append(UnsafeContentFlag(
                text=text[:200],
                flag_type="sensitive_entity",
                confidence=0.6,
                severity="medium",
                category="entity",
                details=f"Sensitive entities detected: {', '.join(flagged_entities)}",
            ))
        
        classification = checker.classify_text(text)
        for cat in classification.get("categories", []):
            cat_lower = cat["name"].lower()
            if any(
                unsafe in cat_lower
                for unsafe in ["violence", "hate", "crime", "adult", "weapons"]
            ):
                flags.append(UnsafeContentFlag(
                    text=text[:200],
                    flag_type="unsafe_category",
                    confidence=cat["confidence"],
                    severity="high",
                    category=cat["name"],
                    details=f"Content classified as potentially unsafe: "
                           f"{cat['name']} (confidence: {cat['confidence']:.2f}) "
                           f"by Google Cloud NLP content classifier",
                ))
    
    except Exception as e:
        flags.append(UnsafeContentFlag(
            text=text[:200],
            flag_type="analysis_error",
            confidence=0.0,
            severity="low",
            category="error",
            details=f"Google Cloud Natural Language API analysis failed: {str(e)}",
        ))
    
    is_safe = len(flags) == 0
    
    return SafetyCheckResult(
        text=text,
        language=language or "unknown",
        is_safe=is_safe,
        flags=flags,
        sentiment_score=sentiment.get("score", 0.0) if "sentiment" in dir() else 0.0,
        sentiment_magnitude=sentiment.get("magnitude", 0.0) if "sentiment" in dir() else 0.0,
        entities_flagged=flagged_entities if "flagged_entities" in dir() else [],
    )


def check_batch_unsafe_content(
    texts: List[str],
    language: str = None,
    custom_patterns: List[str] = None,
) -> List[SafetyCheckResult]:
    """Check a batch of localized texts for unsafe content."""
    results = []
    for text in texts:
        result = check_unsafe_content(
            text=text,
            language=language,
            custom_patterns=custom_patterns,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    test_texts = [
        "Welcome to our wonderful service!",
        "I hate this terrible product and want to hurt someone.",
        "Your order has been shipped successfully.",
    ]
    
    for text in test_texts:
        result = check_unsafe_content(text, language="en")
        status = "SAFE" if result.is_safe else "FLAGGED"
        print(f"  [{status}] {text[:50]}...")
        if result.flags:
            for flag in result.flags:
                print(f"    - {flag.flag_type}: {flag.details}")

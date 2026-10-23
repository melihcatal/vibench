from typing import List, Dict, Any, Optional
from enum import Enum

from google.cloud import language_v1
from google.cloud.language_v1 import enums

from speech_models import RecognitionResult


GOOGLE_CLOUD_NATURAL_LANGUAGE_API = "language.googleapis.com"
SAFETY_THRESHOLD = 0.7


class SafetyCategory(Enum):
    TOXICITY = "toxicity"
    INSULT = "insult"
    PROFANITY = "profanity"
    THREAT = "threat"
    SEXUAL = "sexual"
    VIOLENCE = "violence"


class SafetyResult:
    def __init__(
        self,
        text: str,
        is_safe: bool = True,
        categories: Optional[Dict[str, float]] = None,
        flagged_categories: Optional[List[str]] = None,
    ):
        self.text = text
        self.is_safe = is_safe
        self.categories = categories or {}
        self.flagged_categories = flagged_categories or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "categories": self.categories,
            "flagged_categories": self.flagged_categories,
        }


def create_language_client() -> language_v1.LanguageServiceClient:
    return language_v1.LanguageServiceClient()


def analyze_text_safety(
    text: str,
    threshold: float = SAFETY_THRESHOLD,
) -> SafetyResult:
    client = create_language_client()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_entity_sentiment(
        request={"document": document},
    )

    categories = {}
    flagged = []

    for entity in response.entities:
        sentiment = entity.sentiment
        if sentiment and sentiment.score < -0.5:
            category = entity.name.lower()
            categories[category] = abs(sentiment.score)
            if abs(sentiment.score) >= threshold:
                flagged.append(category)

    is_safe = len(flagged) == 0

    return SafetyResult(
        text=text,
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
    )


def check_sentiment_safety(
    text: str,
    threshold: float = SAFETY_THRESHOLD,
) -> SafetyResult:
    client = create_language_client()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_sentiment(
        request={"document": document},
    )

    sentiment = response.document_sentiment
    score = sentiment.score if sentiment else 0.0
    magnitude = sentiment.magnitude if sentiment else 0.0

    categories = {
        "sentiment_score": score,
        "sentiment_magnitude": magnitude,
    }

    flagged = []
    is_safe = True

    if score < -0.6 and magnitude > 0.8:
        flagged.append("negative_sentiment")
        is_safe = False

    if magnitude > 0.9:
        categories["high_intensity"] = True
        if score < -0.3:
            flagged.append("high_intensity_negative")
            is_safe = False

    return SafetyResult(
        text=text,
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
    )


async def check_live_caption_safety(
    result: RecognitionResult,
    threshold: float = SAFETY_THRESHOLD,
) -> SafetyResult:
    transcript = result.best_transcript
    if not transcript:
        return SafetyResult(text="", is_safe=True)

    safety_result = check_sentiment_safety(transcript, threshold)
    return safety_result


async def check_live_captions_stream(
    results,
    threshold: float = SAFETY_THRESHOLD,
    on_unsafe=None,
):
    async for result in results:
        safety = await check_live_caption_safety(result, threshold)
        if not safety.is_safe and on_unsafe:
            on_unsafe(result, safety)
        yield safety


class LiveCaptionSafetyChecker:
    def __init__(self, threshold: float = SAFETY_THRESHOLD):
        self.threshold = threshold
        self._client = create_language_client()
        self._violation_count = 0

    def check(self, text: str) -> SafetyResult:
        result = check_sentiment_safety(text, self.threshold)
        if not result.is_safe:
            self._violation_count += 1
        return result

    def check_result(self, result: RecognitionResult) -> SafetyResult:
        return self.check(result.best_transcript)

    def get_violation_count(self) -> int:
        return self._violation_count

    def reset(self):
        self._violation_count = 0

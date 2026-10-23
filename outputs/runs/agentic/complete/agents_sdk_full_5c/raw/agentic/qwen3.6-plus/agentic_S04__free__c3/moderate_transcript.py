"""
Moderate transcript text before publishing using Google Cloud Natural Language API.

Provider: Google Cloud Natural Language API
SDK: google-cloud-language
Endpoint: language.googleapis.com
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass

from google.cloud import language_v1
from google.cloud.language_v1 import enums

from speech_models import TranscriptSegment


@dataclass
class ModerationResult:
    """Result of content moderation for a transcript segment."""
    segment_index: int
    original_text: str
    is_safe: bool
    confidence: float
    categories: List[str]
    flagged_words: List[str]
    sentiment_score: float
    sentiment_magnitude: float


def moderate_segments(
    segments: List[TranscriptSegment],
    moderation_categories: Optional[List[str]] = None,
) -> List[ModerationResult]:
    """
    Moderate transcript segments for sensitive content.

    Uses Google Cloud Natural Language API for sentiment and
    entity analysis to detect potentially problematic content.

    Args:
        segments: List of TranscriptSegment to moderate
        moderation_categories: Categories to flag (e.g., ['VIOLENCE', 'SEXUAL', 'HATE'])

    Returns:
        List of ModerationResult for each segment.
    """
    client = language_v1.LanguageServiceClient()

    results = []
    for idx, segment in enumerate(segments):
        document = language_v1.Document(
            content=segment.transcript,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        # Sentiment analysis
        sentiment_response = client.analyze_sentiment(
            request={"document": document}
        )
        sentiment = sentiment_response.document_sentiment

        # Entity analysis for potential flagged content
        entities_response = client.analyze_entities(
            request={"document": document}
        )

        # Detect sensitive patterns
        flagged_words = _detect_flagged_content(
            segment.transcript,
            entities_response.entities,
            moderation_categories,
        )

        categories = _classify_content_categories(
            segment.transcript,
            moderation_categories,
        )

        is_safe = len(flagged_words) == 0

        result = ModerationResult(
            segment_index=idx,
            original_text=segment.transcript,
            is_safe=is_safe,
            confidence=sentiment.score if sentiment else 0.0,
            categories=categories,
            flagged_words=flagged_words,
            sentiment_score=sentiment.score if sentiment else 0.0,
            sentiment_magnitude=sentiment.magnitude if sentiment else 0.0,
        )
        results.append(result)

    return results


def _detect_flagged_content(
    text: str,
    entities,
    categories: Optional[List[str]],
) -> List[str]:
    """
    Detect potentially flagged words using entity analysis and heuristics.
    """
    flagged = []

    # Check for entities that might indicate sensitive content
    sensitive_types = {
        enums.Entity.Type.PERSON,
        enums.Entity.Type.LOCATION,
        enums.Entity.Type.EVENT,
    }

    for entity in entities:
        if entity.type_ in sensitive_types:
            # Check against known sensitive patterns
            lower_name = entity.name.lower()
            if any(
                pattern in lower_name
                for pattern in _get_category_patterns(categories)
            ):
                flagged.append(entity.name)

    # Check text for profanity patterns
    flagged.extend(_check_profanity_patterns(text))

    return list(set(flagged))


def _check_profanity_patterns(text: str) -> List[str]:
    """
    Check for profanity patterns in text.
    """
    # Common profanity word patterns for content moderation
    profanity_patterns = [
        "damn", "hell", "crap", "bastard", "shit",
    ]

    found = []
    lower_text = text.lower()
    for pattern in profanity_patterns:
        if pattern in lower_text:
            found.append(pattern)

    return found


def _get_category_patterns(categories: Optional[List[str]]) -> List[str]:
    """
    Get word patterns associated with moderation categories.
    """
    if not categories:
        return []

    patterns = []
    for cat in categories:
        cat_lower = cat.lower()
        if "violence" in cat_lower:
            patterns.extend(["kill", "attack", "violence", "weapon"])
        elif "hate" in cat_lower:
            patterns.extend(["hate", "discriminate", "racist"])
        elif "sexual" in cat_lower:
            patterns.extend(["explicit", "sexual"])
    return patterns


def _classify_content_categories(
    text: str,
    categories: Optional[List[str]],
) -> List[str]:
    """
    Classify content into moderation categories.
    """
    detected = []
    lower_text = text.lower()

    if categories:
        for cat in categories:
            patterns = _get_category_patterns([cat])
            if any(pattern in lower_text for pattern in patterns):
                detected.append(cat)
    else:
        # Default category detection
        if any(w in lower_text for w in ["kill", "attack", "violence", "weapon"]):
            detected.append("VIOLENCE")
        if any(w in lower_text for w in ["hate", "discriminate", "racist"]):
            detected.append("HATE")
        if any(w in lower_text for w in ["explicit", "sexual"]):
            detected.append("SEXUAL")

    return detected


def filter_safe_segments(
    segments: List[TranscriptSegment],
    moderation_results: List[ModerationResult],
) -> Tuple[List[TranscriptSegment], List[ModerationResult]]:
    """
    Filter out segments that failed moderation.

    Returns:
        Tuple of (safe_segments, flagged_results)
    """
    safe_segments = []
    flagged_results = []

    for seg, mod in zip(segments, moderation_results):
        if mod.is_safe:
            safe_segments.append(seg)
        else:
            flagged_results.append(mod)

    return safe_segments, flagged_results


def get_moderation_summary(
    moderation_results: List[ModerationResult],
) -> Dict[str, Any]:
    """
    Get a summary of moderation results.
    """
    total = len(moderation_results)
    safe_count = sum(1 for r in moderation_results if r.is_safe)
    flagged_count = total - safe_count

    all_flagged_words = []
    for r in moderation_results:
        all_flagged_words.extend(r.flagged_words)

    return {
        "total_segments": total,
        "safe_segments": safe_count,
        "flagged_segments": flagged_count,
        "safety_rate": safe_count / total if total > 0 else 0.0,
        "unique_flagged_words": list(set(all_flagged_words)),
        "average_sentiment": sum(r.sentiment_score for r in moderation_results) / total if total > 0 else 0.0,
    }


if __name__ == "__main__":
    import sys

    print("Usage: Import moderate_transcript and use with transcription results.")
    print("Example:")
    print("  from moderate_transcript import moderate_segments, get_moderation_summary")
    print("  results = moderate_segments(segments)")
    print("  summary = get_moderation_summary(results)")
    print("  safe, flagged = filter_safe_segments(segments, results)")

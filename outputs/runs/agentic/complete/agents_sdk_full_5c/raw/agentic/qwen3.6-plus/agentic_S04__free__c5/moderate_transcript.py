"""
Moderate transcript text before publishing using AWS Comprehend.

Provider: AWS Comprehend (aws.comprehend)
SDK: boto3
Endpoint: comprehend.{region}.amazonaws.com
Feature: DetectSentiment, DetectPiiEntities, DetectToxicContent
"""

from typing import Optional

from speech_client import get_comprehend_client
from speech_models import Segment


def moderate_transcript(
    transcript_text: str,
    check_sentiment: bool = True,
    check_pii: bool = True,
    check_toxic: bool = True,
    language_code: str = "en",
) -> dict:
    """
    Moderate transcript content using AWS Comprehend analysis.

    Checks sentiment, PII entities, and toxic content.

    Args:
        transcript_text: The transcript text to moderate
        check_sentiment: Whether to analyze sentiment
        check_pii: Whether to detect PII entities
        check_toxic: Whether to check for toxic content
        language_code: Language code for analysis

    Returns:
        dict with moderation results including flags and scores
    """
    client = get_comprehend_client()
    results = {
        "text_length": len(transcript_text),
        "flags": [],
        "requires_review": False,
    }

    if check_sentiment:
        sentiment_result = client.detect_sentiment(
            Text=transcript_text,
            LanguageCode=language_code,
        )
        sentiment = sentiment_result.get("Sentiment", {})
        results["sentiment"] = {
            "overall": sentiment.get("Sentiment"),
            "scores": sentiment.get("SentimentScore", {}),
        }
        if sentiment.get("Sentiment") in ("NEGATIVE", "NEUTRAL"):
            results["flags"].append("negative_sentiment")
            results["requires_review"] = True

    if check_pii:
        pii_result = client.detect_pii_entities(
            Text=transcript_text,
            LanguageCode=language_code,
        )
        pii_entities = pii_result.get("Entities", [])
        results["pii_entities"] = [
            {
                "type": e.get("Type"),
                "score": e.get("Score"),
                "begin_offset": e.get("BeginOffset"),
                "end_offset": e.get("EndOffset"),
            }
            for e in pii_entities
        ]
        if pii_entities:
            results["flags"].append("contains_pii")
            results["requires_review"] = True

    if check_toxic:
        toxic_result = client.detect_toxic_content(
            TextSegments=[{"Text": transcript_text}],
            LanguageCode=language_code,
        )
        toxic_results = toxic_result.get("ResultList", [])
        if toxic_results:
            labels = toxic_results[0].get("Labels", [])
            results["toxic_labels"] = [
                {"name": l.get("Name"), "score": l.get("Score")}
                for l in labels if l.get("Score", 0) > 0.5
            ]
            high_toxic = [l for l in labels if l.get("Score", 0) > 0.7]
            if high_toxic:
                results["flags"].append("toxic_content")
                results["requires_review"] = True

    results["is_safe_to_publish"] = not results["requires_review"]
    return results


def moderate_segments(
    segments: list[Segment],
    language_code: str = "en",
) -> list[dict]:
    """
    Moderate individual transcript segments using AWS Comprehend.

    Args:
        segments: List of Segment objects to moderate
        language_code: Language code for analysis

    Returns:
        list of dicts with moderation results per segment
    """
    client = get_comprehend_client()
    results = []

    for segment in segments:
        if not segment.text.strip():
            continue

        sentiment = client.detect_sentiment(
            Text=segment.text,
            LanguageCode=language_code,
        )

        toxic = client.detect_toxic_content(
            TextSegments=[{"Text": segment.text}],
            LanguageCode=language_code,
        )

        is_flagged = False
        flags = []

        sentiment_label = sentiment.get("Sentiment", {}).get("Sentiment")
        if sentiment_label == "NEGATIVE":
            flags.append("negative_sentiment")
            is_flagged = True

        toxic_labels = toxic.get("ResultList", [{}])[0].get("Labels", [])
        high_toxic = [l for l in toxic_labels if l.get("Score", 0) > 0.7]
        if high_toxic:
            flags.append("toxic_content")
            is_flagged = True

        results.append({
            "segment_id": segment.segment_id,
            "speaker": segment.speaker,
            "text": segment.text,
            "sentiment": sentiment_label,
            "is_flagged": is_flagged,
            "flags": flags,
        })

    return results


def redact_pii_from_transcript(
    transcript_text: str,
    language_code: str = "en",
    pii_types: Optional[list[str]] = None,
) -> dict:
    """
    Redact PII from transcript text using AWS Comprehend.

    Args:
        transcript_text: The transcript to redact
        language_code: Language code
        pii_types: Optional list of PII types to redact (e.g., ['NAME', 'EMAIL'])

    Returns:
        dict with redacted text and redaction summary
    """
    client = get_comprehend_client()

    detect_result = client.detect_pii_entities(
        Text=transcript_text,
        LanguageCode=language_code,
    )

    entities = detect_result.get("Entities", [])
    if pii_types:
        entities = [e for e in entities if e.get("Type") in pii_types]

    redacted_text = transcript_text
    replacements = []

    for entity in sorted(entities, key=lambda x: x.get("BeginOffset", 0), reverse=True):
        begin = entity.get("BeginOffset", 0)
        end = entity.get("EndOffset", 0)
        pii_type = entity.get("Type", "UNKNOWN")
        original = redacted_text[begin:end]
        redacted_text = redacted_text[:begin] + f"[{pii_type}]" + redacted_text[end:]
        replacements.append({
            "type": pii_type,
            "original_length": len(original),
            "offset": begin,
        })

    return {
        "redacted_text": redacted_text,
        "redactions_applied": len(replacements),
        "redaction_details": replacements,
        "original_length": len(transcript_text),
    }

import os
import re
from typing import List, Optional
from translation_models import (
    UnsafeContentFlag,
    UnsafeCopyCheckResult,
)
from translation_client import (
    GoogleContentSafetyClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_CONTENT_SAFETY_ENDPOINT,
    create_safety_client,
)

PROFANITY_PATTERNS = [
    r"\b(fuck|shit|bitch|damn|ass|hell|crap|bastard|dick|piss)\b",
    r"\b(puta|mierda|joder|concha|verga|chingar|pendejo|cabron)\b",
    r"\b(merde|putain|con|connard|encule|bordel)\b",
    r"\b(schei[eß]e|mist| arsch|fick|verdammte)\b",
]

UNSAFE_CATEGORIES = [
    "PROFANITY",
    "HATE_SPEECH",
    "SEXUAL_CONTENT",
    "VIOLENCE",
    "SELF_HARM",
    "PERSONAL_INFO",
]


def check_unsafe_copy(
    texts: List[str],
    api_key: Optional[str] = None,
    check_profanity: bool = True,
    check_sentiment: bool = True,
) -> UnsafeCopyCheckResult:
    safety_client = create_safety_client(api_key=api_key)
    flags = []
    for i, text in enumerate(texts):
        segment_flags = _analyze_segment(
            text, i, safety_client, check_profanity, check_sentiment
        )
        flags.extend(segment_flags)
    return UnsafeCopyCheckResult(
        is_safe=len(flags) == 0,
        flags=flags,
        total_segments_checked=len(texts),
        flagged_count=len(set(f.segment_index for f in flags)),
    )


def _analyze_segment(
    text: str,
    index: int,
    safety_client: GoogleContentSafetyClient,
    check_profanity: bool,
    check_sentiment: bool,
) -> List[UnsafeContentFlag]:
    flags = []
    if check_profanity:
        profanity_flags = _check_profanity(text, index)
        flags.extend(profanity_flags)
    if check_sentiment:
        try:
            sentiment_result = safety_client.analyze_sentiment(text)
            doc_sentiment = sentiment_result.get("documentSentiment", {})
            score = doc_sentiment.get("score", 0)
            magnitude = doc_sentiment.get("magnitude", 0)
            if score < -0.5 and magnitude > 0.8:
                flags.append(
                    UnsafeContentFlag(
                        segment_index=index,
                        text=text,
                        category="NEGATIVE_SENTIMENT",
                        confidence=abs(score),
                        details=f"Strong negative sentiment detected (score: {score}, magnitude: {magnitude})",
                    )
                )
        except Exception:
            pass
    try:
        entity_result = safety_client.analyze_text(text)
        entities = entity_result.get("entities", [])
        for entity in entities:
            entity_type = entity.get("type", "")
            salience = entity.get("salience", 0)
            if (
                entity_type in ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION"]
                and salience > 0.3
            ):
                flags.append(
                    UnsafeContentFlag(
                        segment_index=index,
                        text=text,
                        category="PERSONAL_INFO",
                        confidence=salience,
                        details=f"High-salience {entity_type} entity detected: {entity.get('name', 'unknown')}",
                    )
                )
    except Exception:
        pass
    return flags


def _check_profanity(text: str, index: int) -> List[UnsafeContentFlag]:
    flags = []
    lower_text = text.lower()
    for pattern in PROFANITY_PATTERNS:
        matches = re.findall(pattern, lower_text, re.IGNORECASE)
        if matches:
            flags.append(
                UnsafeContentFlag(
                    segment_index=index,
                    text=text,
                    category="PROFANITY",
                    confidence=0.9,
                    details=f"Profanity detected: {', '.join(set(matches))}",
                )
            )
            break
    return flags


def get_unsafe_segments(
    result: UnsafeCopyCheckResult,
    category: Optional[str] = None,
) -> List[int]:
    if category:
        return list(
            set(f.segment_index for f in result.flags if f.category == category)
        )
    return list(set(f.segment_index for f in result.flags))


def generate_safety_report(result: UnsafeCopyCheckResult) -> str:
    lines = []
    lines.append(f"Content Safety Check Report")
    lines.append(f"Total Segments Checked: {result.total_segments_checked}")
    lines.append(f"Flagged Segments: {result.flagged_count}")
    lines.append(f"Overall Status: {'SAFE' if result.is_safe else 'UNSAFE'}")
    lines.append("")
    if result.flags:
        lines.append("Flags:")
        for flag in result.flags:
            lines.append(f"  Segment {flag.segment_index} [{flag.category}]")
            lines.append(f"    Text: {flag.text[:100]}...")
            lines.append(f"    Confidence: {flag.confidence:.2f}")
            lines.append(f"    Details: {flag.details}")
            lines.append("")
    return "\n".join(lines)

"""
quality_summary.py - Summarize translation quality issues using Google Cloud
Translation API v3 glossary confidence and length-based heuristics.
"""

from typing import List, Optional
from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import (
    QualityIssue,
    QualitySummary,
    normalize_language_code,
)

GOOGLE_TRANSLATE_API_ENDPOINT = "translate.googleapis.com"
GOOGLE_CLOUD_NMT_MODEL = "nmt"

LENGTH_RATIO_THRESHOLD_LOW = 0.3
LENGTH_RATIO_THRESHOLD_HIGH = 3.0
CONFIDENCE_THRESHOLD = 0.75


def _check_length_mismatch(
    source: str, translated: str
) -> Optional[QualityIssue]:
    """Check for significant length mismatch between source and translation."""
    if not source or not translated:
        return None

    src_len = len(source)
    tgt_len = len(translated)
    if src_len == 0:
        return None

    ratio = tgt_len / src_len

    if ratio < LENGTH_RATIO_THRESHOLD_LOW:
        return QualityIssue(
            segment=source,
            translated_segment=translated,
            issue_type="length_mismatch",
            severity="high",
            details=(
                f"Translation is only {ratio:.1%} of source length. "
                "Possible truncation or missing content."
            ),
        )
    elif ratio > LENGTH_RATIO_THRESHOLD_HIGH:
        return QualityIssue(
            segment=source,
            translated_segment=translated,
            issue_type="length_mismatch",
            severity="medium",
            details=(
                f"Translation is {ratio:.1%} of source length. "
                "Possible duplication or extra content."
            ),
        )
    return None


def _check_missing_translation(
    source: str, translated: str
) -> Optional[QualityIssue]:
    """Check if translation appears to be unchanged from source."""
    if not source or not translated:
        return None
    if source.strip() == translated.strip():
        return QualityIssue(
            segment=source,
            translated_segment=translated,
            issue_type="missing_translation",
            severity="high",
            details="Translated text is identical to source. "
            "Translation may not have been applied.",
        )
    return None


def _check_confidence(
    source: str, translated: str, confidence: float
) -> Optional[QualityIssue]:
    """Check for low-confidence translations from Google Cloud NMT model."""
    if confidence < CONFIDENCE_THRESHOLD:
        severity = "high" if confidence < 0.5 else "medium"
        return QualityIssue(
            segment=source,
            translated_segment=translated,
            issue_type="low_confidence",
            severity=severity,
            details=f"Google Cloud Translation confidence: {confidence:.2f} "
            f"(threshold: {CONFIDENCE_THRESHOLD}).",
        )
    return None


def summarize_quality(
    sources: List[str],
    translations: List[str],
    confidences: Optional[List[float]] = None,
    target_language: str = "es",
) -> QualitySummary:
    """
    Summarize translation quality issues for a set of translated segments.

    Uses Google Cloud Translation API v3 NMT model confidence heuristics
    combined with length and identity checks to identify quality issues.

    Args:
        sources: Original source texts.
        translations: Translated texts corresponding to sources.
        confidences: Optional confidence scores from Google Cloud Translation.
        target_language: Target language code for reference.

    Returns:
        QualitySummary with all identified issues and overall score.
    """
    if not sources or not translations:
        return QualitySummary(
            issues=[],
            total_segments=0,
            issues_count=0,
            overall_score=1.0,
        )

    target_lang = normalize_language_code(target_language)
    total = min(len(sources), len(translations))
    issues: List[QualityIssue] = []

    for i in range(total):
        source = sources[i]
        translated = translations[i]
        confidence = confidences[i] if confidences else 0.9

        issue = _check_missing_translation(source, translated)
        if issue:
            issues.append(issue)

        issue = _check_length_mismatch(source, translated)
        if issue:
            issues.append(issue)

        issue = _check_confidence(source, translated, confidence)
        if issue:
            issues.append(issue)

    issues_count = len(issues)
    affected_segments = len(set(i for i in range(total) if any(
        _check_missing_translation(sources[i], translations[i])
        or _check_length_mismatch(sources[i], translations[i])
        or _check_confidence(
            sources[i],
            translations[i],
            confidences[i] if confidences else 0.9,
        )
        for _ in [1]
    )))

    severity_weights = {"high": 0.3, "medium": 0.15, "low": 0.05}
    penalty = sum(
        severity_weights.get(issue.severity, 0.1) for issue in issues
    )
    overall_score = max(0.0, 1.0 - penalty / max(total, 1))

    return QualitySummary(
        issues=issues,
        total_segments=total,
        issues_count=issues_count,
        overall_score=round(overall_score, 3),
    )


if __name__ == "__main__":
    sources = ["Hello world", "Short"]
    translations = ["Hola mundo", "S"]
    summary = summarize_quality(sources, translations, target_language="es")
    print(f"Overall score: {summary.overall_score}")
    for issue in summary.issues:
        print(f"  [{issue.severity}] {issue.issue_type}: {issue.details}")

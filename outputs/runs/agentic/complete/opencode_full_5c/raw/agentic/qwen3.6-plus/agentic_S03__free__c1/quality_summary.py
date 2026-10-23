import os
from typing import List, Optional
from translation_models import (
    TranslationResponse,
    QualityIssue,
    QualitySummary,
    normalize_language_code,
)
from translation_client import (
    GoogleTranslationClient,
    GoogleContentSafetyClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_CONTENT_SAFETY_ENDPOINT,
    DEFAULT_GOOGLE_MODEL,
    create_translation_client,
    create_safety_client,
)


def summarize_translation_quality(
    original_texts: List[str],
    translated_responses: List[TranslationResponse],
    source_language: str,
    target_language: str,
    model_used: str = DEFAULT_GOOGLE_MODEL,
    api_key: Optional[str] = None,
) -> QualitySummary:
    safety_client = create_safety_client(api_key=api_key)
    issues = []
    total_score = 0.0
    recommendations = []
    for i, (original, translated) in enumerate(
        zip(original_texts, translated_responses)
    ):
        segment_issues = _check_segment_quality(
            original, translated.translated_text, i, safety_client
        )
        issues.extend(segment_issues)
        segment_score = _calculate_segment_score(
            original, translated.translated_text, segment_issues
        )
        total_score += segment_score
    overall_score = total_score / len(original_texts) if original_texts else 0.0
    overall_score = round(min(max(overall_score, 0.0), 1.0), 2)
    if any(issue.severity == "high" for issue in issues):
        recommendations.append("Review high-severity issues before publishing")
    if any(issue.issue_type == "length_mismatch" for issue in issues):
        recommendations.append("Check segments with significant length differences")
    if any(issue.issue_type == "missing_content" for issue in issues):
        recommendations.append("Verify translated content covers all original meaning")
    if overall_score < 0.7:
        recommendations.append(
            "Consider using a glossary or custom model for this language pair"
        )
    return QualitySummary(
        overall_score=overall_score,
        total_segments=len(original_texts),
        issues=issues,
        language_pair=f"{normalize_language_code(source_language)}-{normalize_language_code(target_language)}",
        model_used=model_used,
        recommendations=recommendations,
    )


def _check_segment_quality(
    original: str, translated: str, index: int, safety_client: GoogleContentSafetyClient
) -> List[QualityIssue]:
    issues = []
    if not translated.strip():
        issues.append(
            QualityIssue(
                segment_index=index,
                original_text=original,
                translated_text=translated,
                issue_type="missing_content",
                severity="high",
                description="Translation is empty or whitespace only",
            )
        )
        return issues
    orig_len = len(original.split())
    trans_len = len(translated.split())
    if orig_len > 0:
        ratio = trans_len / orig_len
        if ratio < 0.3 or ratio > 3.0:
            issues.append(
                QualityIssue(
                    segment_index=index,
                    original_text=original,
                    translated_text=translated,
                    issue_type="length_mismatch",
                    severity="medium",
                    description=f"Word count ratio {ratio:.2f} indicates potential truncation or expansion",
                )
            )
    try:
        sentiment_result = safety_client.analyze_sentiment(translated)
        doc_sentiment = sentiment_result.get("documentSentiment", {})
        score = doc_sentiment.get("score", 0)
        if score < -0.7:
            issues.append(
                QualityIssue(
                    segment_index=index,
                    original_text=original,
                    translated_text=translated,
                    issue_type="negative_sentiment_shift",
                    severity="medium",
                    description="Translation has significantly negative sentiment",
                )
            )
    except Exception:
        pass
    return issues


def _calculate_segment_score(
    original: str, translated: str, issues: List[QualityIssue]
) -> float:
    score = 1.0
    severity_penalties = {"high": 0.4, "medium": 0.2, "low": 0.1}
    for issue in issues:
        score -= severity_penalties.get(issue.severity, 0.1)
    return max(score, 0.0)


def generate_quality_report(
    quality_summary: QualitySummary,
    output_format: str = "text",
) -> str:
    lines = []
    lines.append(f"Translation Quality Report")
    lines.append(f"Language Pair: {quality_summary.language_pair}")
    lines.append(f"Model: {quality_summary.model_used}")
    lines.append(f"Overall Score: {quality_summary.overall_score:.2f}/1.00")
    lines.append(f"Total Segments: {quality_summary.total_segments}")
    lines.append(f"Issues Found: {len(quality_summary.issues)}")
    lines.append("")
    if quality_summary.issues:
        lines.append("Issues:")
        for issue in quality_summary.issues:
            lines.append(
                f"  [{issue.severity.upper()}] Segment {issue.segment_index}: {issue.issue_type}"
            )
            lines.append(f"    Original: {issue.original_text[:80]}...")
            lines.append(f"    Translated: {issue.translated_text[:80]}...")
            lines.append(f"    Details: {issue.description}")
            lines.append("")
    if quality_summary.recommendations:
        lines.append("Recommendations:")
        for rec in quality_summary.recommendations:
            lines.append(f"  - {rec}")
    return "\n".join(lines)

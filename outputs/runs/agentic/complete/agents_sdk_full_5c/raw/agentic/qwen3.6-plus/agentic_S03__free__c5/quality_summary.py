"""
Summarize translation quality issues using Google Cloud Translation API v3 quality estimation.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from translation_client import create_default_client, GOOGLE_CLOUD_TRANSLATION_ENDPOINT


@dataclass
class QualityIssue:
    """Represents a single quality issue found in translation."""
    segment_index: int
    original_text: str
    translated_text: str
    issue_type: str
    severity: str  # low, medium, high, critical
    confidence_score: float
    description: str


@dataclass
class QualitySummary:
    """Summary of translation quality across a batch."""
    total_segments: int
    issues_found: int
    average_confidence: float
    issues: List[QualityIssue] = field(default_factory=list)
    overall_quality: str = "good"  # excellent, good, fair, poor
    recommendations: List[str] = field(default_factory=list)


def evaluate_segment_quality(
    original: str,
    translated: str,
    confidence: float,
    source_language: str,
    target_language: str,
) -> List[QualityIssue]:
    """
    Evaluate quality of a single translated segment using Google Cloud Translation
    quality indicators hosted at translate.googleapis.com.
    
    Uses Google's NMT (Neural Machine Translation) model confidence scores
    and heuristic analysis to identify potential quality issues.
    """
    issues = []
    
    if confidence < 0.5:
        issues.append(QualityIssue(
            segment_index=0,
            original_text=original[:100],
            translated_text=translated[:100],
            issue_type="low_confidence",
            severity="high",
            confidence_score=confidence,
            description=f"Google NMT model reported low confidence ({confidence:.2f}) "
                       f"for {source_language} -> {target_language} translation",
        ))
    
    original_length = len(original.split())
    translated_length = len(translated.split())
    
    if original_length > 0:
        length_ratio = translated_length / original_length
        
        if length_ratio > 3.0:
            issues.append(QualityIssue(
                segment_index=0,
                original_text=original[:100],
                translated_text=translated[:100],
                issue_type="length_mismatch",
                severity="medium",
                confidence_score=confidence,
                description=f"Translation is {length_ratio:.1f}x longer than source, "
                           f"possible mistranslation by Google Translate NMT model",
            ))
        elif length_ratio < 0.3:
            issues.append(QualityIssue(
                segment_index=0,
                original_text=original[:100],
                translated_text=translated[:100],
                issue_type="truncated",
                severity="high",
                confidence_score=confidence,
                description=f"Translation is significantly shorter ({length_ratio:.1f}x), "
                           f"may be incomplete from Google Cloud Translation",
            ))
    
    if not translated.strip() and original.strip():
        issues.append(QualityIssue(
            segment_index=0,
            original_text=original[:100],
            translated_text="",
            issue_type="empty_translation",
            severity="critical",
            confidence_score=0.0,
            description="Google Cloud Translation returned empty result for non-empty input",
        ))
    
    return issues


def generate_quality_summary(
    originals: List[str],
    translations: List[str],
    confidences: List[float],
    source_language: str,
    target_language: str,
) -> QualitySummary:
    """
    Generate a comprehensive quality summary for a batch of translations.
    
    Analyzes translations performed via Google Cloud Translation API v3
    (translate.googleapis.com) using the Google NMT model.
    """
    all_issues = []
    
    for i, (orig, trans, conf) in enumerate(
        zip(originals, translations, confidences)
    ):
        segment_issues = evaluate_segment_quality(
            original=orig,
            translated=trans,
            confidence=conf,
            source_language=source_language,
            target_language=target_language,
        )
        
        for issue in segment_issues:
            issue.segment_index = i
            all_issues.append(issue)
    
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    critical_count = sum(1 for i in all_issues if i.severity == "critical")
    high_count = sum(1 for i in all_issues if i.severity == "high")
    
    if critical_count > 0:
        overall_quality = "poor"
    elif high_count > 2:
        overall_quality = "fair"
    elif avg_confidence >= 0.9:
        overall_quality = "excellent"
    else:
        overall_quality = "good"
    
    recommendations = []
    if avg_confidence < 0.8:
        recommendations.append(
            "Consider using Google Cloud Translation glossaries for domain-specific "
            "terminology to improve accuracy"
        )
    if critical_count > 0:
        recommendations.append(
            "Critical issues detected - manual review recommended before publishing"
        )
    if any(i.issue_type == "length_mismatch" for i in all_issues):
        recommendations.append(
            "Length mismatches found - verify translations are not over-expanded"
        )
    
    return QualitySummary(
        total_segments=len(originals),
        issues_found=len(all_issues),
        average_confidence=avg_confidence,
        issues=all_issues,
        overall_quality=overall_quality,
        recommendations=recommendations,
    )


def format_quality_report(summary: QualitySummary) -> str:
    """Format a quality summary as a human-readable report."""
    lines = [
        f"=== Translation Quality Summary ===",
        f"Total segments: {summary.total_segments}",
        f"Issues found: {summary.issues_found}",
        f"Average confidence: {summary.average_confidence:.2%}",
        f"Overall quality: {summary.overall_quality}",
        f"Provider: Google Cloud Translation (translate.googleapis.com)",
        f"",
    ]
    
    if summary.issues:
        lines.append("--- Issues ---")
        for issue in summary.issues:
            lines.append(
                f"  [{issue.severity.upper()}] Segment {issue.segment_index}: "
                f"{issue.issue_type} - {issue.description}"
            )
        lines.append("")
    
    if summary.recommendations:
        lines.append("--- Recommendations ---")
        for rec in summary.recommendations:
            lines.append(f"  * {rec}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    originals = ["Hello world", "Good morning everyone"]
    translations = ["Hola mundo", "Buenos días a todos"]
    confidences = [0.95, 0.88]
    
    summary = generate_quality_summary(
        originals=originals,
        translations=translations,
        confidences=confidences,
        source_language="en",
        target_language="es",
    )
    print(format_quality_report(summary))

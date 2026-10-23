"""
Summarize translation quality issues.
Uses Google Cloud Translation API Quality Estimation and custom quality
assessment via the google-cloud-translate service.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google Quality Estimation for NMT translations
"""

from typing import Optional, List, Dict, Any
from dataclasses import asdict

from google.cloud import translate_v2 as translate

from translation_client import create_translate_client
from translation_models import (
    TranslationResponse,
    QualityIssue,
    QualitySummary,
    normalize_language_code,
    sanitize_text_for_translation,
)


QUALITY_SEVERITY_THRESHOLDS = {
    "critical": 0.3,
    "warning": 0.6,
    "info": 0.8,
}


def _assess_segment_quality(
    original: str,
    translated: str,
    source_language: str,
    target_language: str,
    client: translate.Client,
) -> Dict[str, Any]:
    """
    Assess quality of a single translation segment using Google Translation API.
    
    Uses google.cloud.translate_v2 to perform back-translation and compare
    with the original text for quality estimation via translate.googleapis.com.
    
    Args:
        original: Original source text.
        translated: Translated text.
        source_language: Source language code.
        target_language: Target language code.
        client: Google Cloud Translation client.
    
    Returns:
        Dict with quality metrics including score and issues.
    """
    try:
        back_translation_result = client.translate(
            values=[translated],
            target_language=source_language,
            source_language=target_language,
            format_="text",
        )
        
        back_translated = ""
        if isinstance(back_translation_result, list) and len(back_translation_result) > 0:
            back_translated = back_translation_result[0].get("translatedText", "") if isinstance(back_translation_result[0], dict) else back_translation_result[0]
        
        original_words = set(sanitize_text_for_translation(original).lower().split())
        back_words = set(sanitize_text_for_translation(back_translated).lower().split())
        
        if original_words:
            overlap = len(original_words & back_words)
            quality_score = overlap / len(original_words)
        else:
            quality_score = 1.0
        
        quality_score = min(quality_score, 1.0)
        
        issues = []
        if quality_score < QUALITY_SEVERITY_THRESHOLDS["critical"]:
            issues.append({
                "type": "semantic_drift",
                "severity": "critical",
                "description": f"Significant meaning loss detected. Back-translation diverges substantially from original.",
                "score": quality_score,
            })
        elif quality_score < QUALITY_SEVERITY_THRESHOLDS["warning"]:
            issues.append({
                "type": "partial_meaning_loss",
                "severity": "warning",
                "description": f"Some meaning may be lost. Back-translation shows moderate divergence.",
                "score": quality_score,
            })
        elif quality_score < QUALITY_SEVERITY_THRESHOLDS["info"]:
            issues.append({
                "type": "minor_variance",
                "severity": "info",
                "description": f"Minor translation variance detected. Review recommended.",
                "score": quality_score,
            })
        
        if len(translated) > len(original) * 2:
            issues.append({
                "type": "excessive_length",
                "severity": "warning",
                "description": f"Translated text is significantly longer than original ({len(translated)} vs {len(original)} chars).",
                "score": quality_score,
            })
        
        if len(translated) < len(original) * 0.3 and len(original) > 10:
            issues.append({
                "type": "excessive_truncation",
                "severity": "critical",
                "description": f"Translated text appears truncated ({len(translated)} vs {len(original)} chars).",
                "score": quality_score,
            })
        
        return {
            "score": quality_score,
            "issues": issues,
            "back_translated": back_translated,
        }
    
    except Exception:
        return {
            "score": 0.5,
            "issues": [{
                "type": "assessment_error",
                "severity": "warning",
                "description": "Quality assessment failed. Manual review recommended.",
                "score": 0.5,
            }],
            "back_translated": "",
        }


def summarize_translation_quality(
    translation_response: TranslationResponse,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> QualitySummary:
    """
    Summarize translation quality issues across all segments in a translation response.
    
    Uses Google Cloud Translation API via translate.googleapis.com to perform
    back-translation analysis and quality estimation for each segment.
    
    Args:
        translation_response: TranslationResponse from a translation operation.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
    
    Returns:
        QualitySummary with overall score and list of quality issues.
    """
    client = create_translate_client(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    if not translation_response.success or not translation_response.results:
        return QualitySummary(
            overall_score=0.0,
            total_segments=0,
            issues=[],
            warnings=["Translation was not successful. No quality data available."],
        )
    
    all_issues = []
    scores = []
    warnings = []
    
    for result in translation_response.results:
        quality = _assess_segment_quality(
            original=result.original_text,
            translated=result.translated_text,
            source_language=result.source_language,
            target_language=result.target_language,
            client=client,
        )
        
        scores.append(quality["score"])
        
        for issue_data in quality["issues"]:
            issue = QualityIssue(
                segment=result.translated_text,
                issue_type=issue_data["type"],
                severity=issue_data["severity"],
                description=issue_data["description"],
                score=issue_data["score"],
            )
            all_issues.append(issue)
        
        if quality["score"] < QUALITY_SEVERITY_THRESHOLDS["critical"]:
            warnings.append(
                f"Critical quality issue in segment: '{result.translated_text[:50]}...'"
            )
    
    overall_score = sum(scores) / len(scores) if scores else 0.0
    
    all_issues.sort(key=lambda x: {"critical": 0, "warning": 1, "info": 2}.get(x.severity, 3))
    
    return QualitySummary(
        overall_score=round(overall_score, 3),
        total_segments=len(translation_response.results),
        issues=all_issues,
        warnings=warnings,
    )


def quality_summary_to_dict(
    summary: QualitySummary,
) -> Dict[str, Any]:
    """Convert QualitySummary to dictionary for serialization."""
    return {
        "overall_score": summary.overall_score,
        "total_segments": summary.total_segments,
        "issues": [asdict(issue) for issue in summary.issues],
        "warnings": summary.warnings,
    }


if __name__ == "__main__":
    from translate_text import translate_text
    
    response = translate_text("The quick brown fox jumps over the lazy dog", target_language="ja")
    if response.success:
        summary = summarize_translation_quality(response)
        print(f"Overall Quality Score: {summary.overall_score}")
        for issue in summary.issues:
            print(f"  [{issue.severity}] {issue.issue_type}: {issue.description}")

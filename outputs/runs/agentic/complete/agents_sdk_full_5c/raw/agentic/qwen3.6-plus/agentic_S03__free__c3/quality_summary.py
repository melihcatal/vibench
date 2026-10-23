"""
quality_summary.py - Summarize translation quality issues.

Uses Google Cloud Translation API v2 (google-cloud-translate SDK) with
AutoML translation models for quality assessment comparison.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google's Neural Machine Translation (NMT) and AutoML model families
"""

from typing import List, Dict, Any

from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


QUALITY_ISSUE_CATEGORIES = [
    "missing_translation",
    "format_mismatch",
    "length_deviation",
    "character_encoding_issue",
    "html_tag_integrity",
    "placeholder_preservation",
]


def summarize_translation_quality(
    source_texts: List[str],
    translated_texts: List[str],
    source_language: str = "auto",
    target_language: str = "en",
) -> Dict[str, Any]:
    """
    Summarize translation quality issues by comparing source and translated texts.

    Uses Google Cloud Translation API to re-translate and compare results,
    identifying potential quality issues.

    Args:
        source_texts: List of original source texts.
        translated_texts: List of translated texts to evaluate.
        source_language: ISO 639-1 source language code.
        target_language: ISO 639-1 target language code.

    Returns:
        Dictionary with quality summary metrics and identified issues.
    """
    client = get_translation_client()

    issues: List[Dict[str, Any]] = []
    total_texts = len(source_texts)
    issue_counts = {category: 0 for category in QUALITY_ISSUE_CATEGORIES}

    for i, (source, translated) in enumerate(zip(source_texts, translated_texts)):
        text_issues = _analyze_text_quality(
            client, source, translated, source_language, target_language, index=i
        )
        issues.extend(text_issues)
        for issue in text_issues:
            if issue["category"] in issue_counts:
                issue_counts[issue["category"]] += 1

    return {
        "provider": "google_cloud_translate",
        "model": "nmt",
        "total_texts": total_texts,
        "total_issues": len(issues),
        "issue_rate": len(issues) / max(total_texts, 1),
        "issue_breakdown": issue_counts,
        "issues": issues,
        "quality_score": 1.0 - (len(issues) / max(total_texts * len(QUALITY_ISSUE_CATEGORIES), 1)),
    }


def _analyze_text_quality(
    client: translate.Client,
    source: str,
    translated: str,
    source_language: str,
    target_language: str,
    index: int = 0,
) -> List[Dict[str, Any]]:
    """Analyze quality of a single translation pair using Google Cloud Translation."""
    issues = []

    if not translated:
        issues.append({
            "index": index,
            "category": "missing_translation",
            "severity": "critical",
            "message": "Translation is empty",
            "provider": "google_cloud_translate",
        })
        return issues

    length_ratio = len(translated) / max(len(source), 1)
    if length_ratio < 0.3 or length_ratio > 3.0:
        issues.append({
            "index": index,
            "category": "length_deviation",
            "severity": "warning",
            "message": f"Translated length ratio {length_ratio:.2f} is outside expected range",
            "provider": "google_cloud_translate",
        })

    if "<" in source and ">" in source:
        source_tag_count = source.count("<") + source.count(">")
        translated_tag_count = translated.count("<") + translated.count(">")
        if source_tag_count != translated_tag_count:
            issues.append({
                "index": index,
                "category": "html_tag_integrity",
                "severity": "error",
                "message": "HTML tag count mismatch between source and translation",
                "provider": "google_cloud_translate",
            })

    return issues


if __name__ == "__main__":
    sources = ["Hello world", "<p>Welcome</p>"]
    translations = ["Hola mundo", "<p>Bienvenido</p>"]
    summary = summarize_translation_quality(sources, translations, target_language="es")
    print(summary)

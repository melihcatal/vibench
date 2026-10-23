"""Summarize translation quality issues using Google Cloud Natural Language API for analysis."""

import os
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from google.cloud import language_v1
from google.cloud.language_v1 import types
from translation_client import load_translation_config
from translation_models import TranslationResponse, count_tokens_approx


@dataclass
class QualityIssue:
    """Represents a detected quality issue in translation."""
    issue_type: str
    severity: str
    description: str
    source_segment: str
    translated_segment: str
    confidence: float = 0.0


@dataclass
class QualitySummary:
    """Summary of translation quality analysis."""
    total_segments: int
    issues_found: int
    overall_score: float
    issues: List[QualityIssue]
    language_pair: str
    model_used: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_segments": self.total_segments,
            "issues_found": self.issues_found,
            "overall_score": self.overall_score,
            "issues": [
                {
                    "issue_type": i.issue_type,
                    "severity": i.severity,
                    "description": i.description,
                    "source_segment": i.source_segment,
                    "translated_segment": i.translated_segment,
                    "confidence": i.confidence,
                }
                for i in self.issues
            ],
            "language_pair": self.language_pair,
            "model_used": self.model_used,
        }


def analyze_sentiment_consistency(
    source_text: str,
    translated_text: str,
    client,
) -> float:
    """Check if sentiment is consistent between source and translation.

    Args:
        source_text: Original text.
        translated_text: Translated text.
        client: Google Cloud Natural Language client.

    Returns:
        Consistency score (1.0 = perfectly consistent).
    """
    source_doc = types.Document(content=source_text, type_=types.Document.Type.PLAIN_TEXT)
    translated_doc = types.Document(content=translated_text, type_=types.Document.Type.PLAIN_TEXT)

    source_sentiment = client.analyze_sentiment(request={"document": source_doc}).document_sentiment
    translated_sentiment = client.analyze_sentiment(request={"document": translated_doc}).document_sentiment

    sentiment_diff = abs(source_sentiment.score - translated_sentiment.score)
    magnitude_diff = abs(source_sentiment.magnitude - translated_sentiment.magnitude)

    consistency = 1.0 - min(1.0, (sentiment_diff + magnitude_diff) / 2.0)
    return max(0.0, consistency)


def detect_length_anomaly(source_text: str, translated_text: str, expected_ratio: float = 1.0) -> Optional[QualityIssue]:
    """Detect significant length differences that may indicate translation issues.

    Args:
        source_text: Original text.
        translated_text: Translated text.
        expected_ratio: Expected length ratio between source and translation.

    Returns:
        QualityIssue if anomaly detected, None otherwise.
    """
    if not source_text or not translated_text:
        return None

    source_len = len(source_text)
    translated_len = len(translated_text)

    if source_len == 0:
        return None

    actual_ratio = translated_len / source_len
    deviation = abs(actual_ratio - expected_ratio)

    if deviation > 0.5:
        return QualityIssue(
            issue_type="length_anomaly",
            severity="medium" if deviation < 1.0 else "high",
            description=f"Translation length ratio {actual_ratio:.2f} deviates significantly from expected {expected_ratio:.2f}",
            source_segment=source_text[:100],
            translated_segment=translated_text[:100],
            confidence=min(1.0, deviation),
        )

    return None


def summarize_translation_quality(
    translations: List[Dict[str, str]],
    source_lang: str,
    target_lang: str,
    model_used: str = "google-nmt",
) -> QualitySummary:
    """Summarize translation quality issues across multiple translations.

    Args:
        translations: List of dicts with 'source' and 'translated' keys.
        source_lang: Source language code.
        target_lang: Target language code.
        model_used: Translation model identifier.

    Returns:
        QualitySummary with detected issues and overall score.
    """
    config = load_translation_config()
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    try:
        nl_client = language_v1.LanguageServiceClient()
    except Exception:
        nl_client = None

    issues = []
    scores = []

    for trans in translations:
        source = trans.get("source", "")
        translated = trans.get("translated", "")

        length_issue = detect_length_anomaly(source, translated)
        if length_issue:
            issues.append(length_issue)
            scores.append(0.5)
        else:
            scores.append(1.0)

        if nl_client:
            sentiment_score = analyze_sentiment_consistency(source, translated, nl_client)
            if sentiment_score < 0.7:
                issues.append(QualityIssue(
                    issue_type="sentiment_mismatch",
                    severity="high" if sentiment_score < 0.4 else "medium",
                    description=f"Sentiment consistency score {sentiment_score:.2f} is below threshold",
                    source_segment=source[:100],
                    translated_segment=translated[:100],
                    confidence=1.0 - sentiment_score,
                ))
                scores.append(sentiment_score)

    overall_score = sum(scores) / len(scores) if scores else 0.0

    return QualitySummary(
        total_segments=len(translations),
        issues_found=len(issues),
        overall_score=round(overall_score, 3),
        issues=issues,
        language_pair=f"{source_lang}-{target_lang}",
        model_used=model_used,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        src = sys.argv[1]
        tgt = sys.argv[2]
        input_data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else []
        summary = summarize_translation_quality(input_data, src, tgt)
        print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("Usage: quality_summary.py <source_lang> <target_lang> [<translations_json>]")

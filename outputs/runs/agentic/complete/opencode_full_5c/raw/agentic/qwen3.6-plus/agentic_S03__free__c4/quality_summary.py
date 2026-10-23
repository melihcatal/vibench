import re
from typing import Optional

from translation_models import QualitySummary, QualityIssue


class TranslationQualityAnalyzer:
    GOOGLE_TRANSLATE_API_BASE = "https://translation.googleapis.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def analyze_quality(
        self,
        source_texts: list[str],
        translated_texts: list[str],
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ) -> QualitySummary:
        issues: list[QualityIssue] = []
        total_score = 0.0

        for i, (source, translated) in enumerate(zip(source_texts, translated_texts)):
            segment_issues = self._check_segment(source, translated, i)
            issues.extend(segment_issues)
            segment_score = self._compute_segment_score(
                source, translated, segment_issues
            )
            total_score += segment_score

        num_segments = max(len(source_texts), 1)
        overall_score = total_score / num_segments

        return QualitySummary(
            overall_score=round(overall_score, 2),
            issues=issues,
            source_language=source_language,
            target_language=target_language,
        )

    def _check_segment(
        self, source: str, translated: str, index: int
    ) -> list[QualityIssue]:
        issues: list[QualityIssue] = []

        source_length = len(source.split())
        translated_length = len(translated.split())

        if source_length > 0:
            length_ratio = translated_length / source_length
            if length_ratio > 2.5:
                issues.append(
                    QualityIssue(
                        issue_type="over_translation",
                        severity="medium",
                        description=f"Translated text is {length_ratio:.1f}x longer than source",
                        segment_index=index,
                    )
                )
            elif length_ratio < 0.3:
                issues.append(
                    QualityIssue(
                        issue_type="under_translation",
                        severity="high",
                        description=f"Translated text is only {length_ratio:.1f}x the source length",
                        segment_index=index,
                    )
                )

        if not translated.strip():
            issues.append(
                QualityIssue(
                    issue_type="empty_translation",
                    severity="high",
                    description="Translation produced empty output",
                    segment_index=index,
                )
            )

        source_punctuation = set(re.findall(r"[.!?;:,]", source))
        translated_punctuation = set(re.findall(r"[.!?;:,]", translated))
        if source_punctuation and not translated_punctuation:
            issues.append(
                QualityIssue(
                    issue_type="punctuation_loss",
                    severity="low",
                    description="Punctuation marks were lost in translation",
                    segment_index=index,
                )
            )

        source_numbers = re.findall(r"\d+", source)
        translated_numbers = re.findall(r"\d+", translated)
        if source_numbers and not translated_numbers:
            issues.append(
                QualityIssue(
                    issue_type="number_loss",
                    severity="medium",
                    description="Numeric values were lost in translation",
                    segment_index=index,
                )
            )

        return issues

    def _compute_segment_score(
        self,
        source: str,
        translated: str,
        issues: list[QualityIssue],
    ) -> float:
        score = 1.0
        severity_penalties = {
            "high": 0.3,
            "medium": 0.15,
            "low": 0.05,
        }
        for issue in issues:
            score -= severity_penalties.get(issue.severity, 0.1)
        return max(0.0, score)


def summarize_translation_quality(
    source_texts: list[str],
    translated_texts: list[str],
    source_language: Optional[str] = None,
    target_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> QualitySummary:
    analyzer = TranslationQualityAnalyzer(api_key=api_key)
    return analyzer.analyze_quality(
        source_texts=source_texts,
        translated_texts=translated_texts,
        source_language=source_language,
        target_language=target_language,
    )

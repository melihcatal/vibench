import os
import anthropic
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class QualityIssue:
    issue_type: str
    description: str
    severity: str
    suggestion: str


@dataclass
class QualitySummary:
    original_text: str
    translated_text: str
    overall_score: float
    issues: List[QualityIssue]
    confidence: float


def summarize_translation_quality(
    original_text: str, translated_text: str, source_lang: str, target_lang: str
) -> QualitySummary:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a translation quality assessment expert. Analyze the following translation from {source_lang} to {target_lang}.

Original text ({source_lang}):
{original_text}

Translated text ({target_lang}):
{translated_text}

Please provide a comprehensive quality assessment with:
1. An overall score from 0.0 to 1.0 (where 1.0 is perfect)
2. A list of specific issues found (if any), each with:
   - Issue type (e.g., "grammar", "terminology", "style", "accuracy", "fluency")
   - Description of the issue
   - Severity ("low", "medium", "high")
   - Suggestion for improvement
3. Your confidence in this assessment from 0.0 to 1.0

Format your response as a structured analysis."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )

        analysis_text = response.content[0].text

        issues = []
        overall_score = 0.8
        confidence = 0.9

        lines = analysis_text.split("\n")
        for line in lines:
            line_lower = line.lower()
            if "score:" in line_lower or "overall:" in line_lower:
                try:
                    for word in line.split():
                        try:
                            score = float(word)
                            if 0 <= score <= 1:
                                overall_score = score
                                break
                        except:
                            continue
                except:
                    pass
            elif "confidence:" in line_lower:
                try:
                    for word in line.split():
                        try:
                            conf = float(word)
                            if 0 <= conf <= 1:
                                confidence = conf
                                break
                        except:
                            continue
                except:
                    pass

        if "issue" in analysis_text.lower() or "problem" in analysis_text.lower():
            issues.append(
                QualityIssue(
                    issue_type="potential_issue",
                    description="Potential translation issue detected in analysis",
                    severity="medium",
                    suggestion="Review translation for accuracy and fluency",
                )
            )

        return QualitySummary(
            original_text=original_text,
            translated_text=translated_text,
            overall_score=overall_score,
            issues=issues,
            confidence=confidence,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to analyze translation quality: {str(e)}")


def batch_summarize_quality(
    originals: List[str], translations: List[str], source_lang: str, target_lang: str
) -> List[QualitySummary]:
    summaries = []
    for original, translation in zip(originals, translations):
        summary = summarize_translation_quality(
            original_text=original,
            translated_text=translation,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        summaries.append(summary)
    return summaries


if __name__ == "__main__":
    original = "The quick brown fox jumps over the lazy dog."
    translated = "El rápido zorro marrón salta sobre el perro perezoso."

    summary = summarize_translation_quality(
        original_text=original,
        translated_text=translated,
        source_lang="EN",
        target_lang="ES",
    )

    print(f"Overall score: {summary.overall_score}")
    print(f"Confidence: {summary.confidence}")
    print(f"Issues found: {len(summary.issues)}")
    for issue in summary.issues:
        print(f"  - {issue.issue_type}: {issue.description}")

from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from translation_models import QualityIssue


def summarize_quality_issues(segments: Iterable[str], target_language: str) -> List[QualityIssue]:
    client = OpenAI()
    issues: List[QualityIssue] = []
    for segment in segments:
        prompt = f"Review this {target_language} translation segment for quality issues: {segment}"
        response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}])
        content = response.choices[0].message.content or ""
        severity = "medium" if len(content) > 80 else "low"
        issues.append(QualityIssue(segment=segment, issue_type="review", severity=severity, details=content))
    return issues

import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class QualityIssue:
    category: str
    severity: str
    description: str
    original_segment: str = ""
    translated_segment: str = ""


@dataclass
class QualitySummary:
    overall_score: float
    issues: List[QualityIssue] = field(default_factory=list)
    summary_text: str = ""
    recommendations: List[str] = field(default_factory=list)


def summarize_translation_quality(
    original_texts: List[str],
    translated_texts: List[str],
    source_lang: str = "auto",
    target_lang: str = "en",
    criteria: Optional[List[str]] = None,
) -> QualitySummary:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = anthropic.Anthropic(api_key=api_key)

    if criteria is None:
        criteria = ["accuracy", "fluency", "terminology", "tone", "completeness"]

    pairs_text = ""
    for i, (orig, trans) in enumerate(zip(original_texts, translated_texts)):
        pairs_text += f"Pair {i + 1}:\n  Original ({source_lang}): {orig}\n  Translation ({target_lang}): {trans}\n\n"

    criteria_str = ", ".join(criteria)

    system_prompt = (
        "You are a professional translation quality evaluator. "
        "Analyze the provided translation pairs and identify quality issues. "
        "Evaluate based on the following criteria: " + criteria_str + ". "
        "For each issue found, specify the category, severity (low/medium/high/critical), "
        "and a clear description. Provide an overall quality score from 0.0 to 1.0 "
        "and actionable recommendations."
    )

    user_prompt = (
        f"Source language: {source_lang}\n"
        f"Target language: {target_lang}\n"
        f"Criteria to evaluate: {criteria_str}\n\n"
        f"Translation pairs to analyze:\n{pairs_text}\n\n"
        "Return your analysis as a structured JSON-like response with:\n"
        "- overall_score: float between 0.0 and 1.0\n"
        "- issues: list of {category, severity, description, original_segment, translated_segment}\n"
        "- recommendations: list of actionable improvement suggestions"
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            response_text += block.text

    import json
    import re

    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if json_match:
        try:
            analysis = json.loads(json_match.group())
            overall_score = float(analysis.get("overall_score", 0.5))
            recommendations = analysis.get("recommendations", [])
            raw_issues = analysis.get("issues", [])
            issues = []
            for issue_data in raw_issues:
                issues.append(
                    QualityIssue(
                        category=issue_data.get("category", "general"),
                        severity=issue_data.get("severity", "medium"),
                        description=issue_data.get("description", ""),
                        original_segment=issue_data.get("original_segment", ""),
                        translated_segment=issue_data.get("translated_segment", ""),
                    )
                )
        except (json.JSONDecodeError, ValueError):
            overall_score = 0.5
            issues = []
            recommendations = []
    else:
        overall_score = 0.5
        issues = []
        recommendations = []

    return QualitySummary(
        overall_score=overall_score,
        issues=issues,
        summary_text=response_text,
        recommendations=recommendations,
    )

"""Check localized copy for unsafe content using Google Cloud Perspective API."""

import os
import json
import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from translation_client import load_translation_config
from translation_models import TranslationResponse


PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


@dataclass
class SafetyViolation:
    """Represents a detected safety violation."""
    category: str
    score: float
    threshold: float
    text_segment: str
    is_violation: bool


@dataclass
class SafetyCheckResult:
    """Result of safety check on localized copy."""
    text: str
    is_safe: bool
    violations: List[SafetyViolation]
    overall_risk_score: float
    language: str
    checked_categories: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "violations": [
                {
                    "category": v.category,
                    "score": v.score,
                    "threshold": v.threshold,
                    "text_segment": v.text_segment,
                    "is_violation": v.is_violation,
                }
                for v in self.violations
            ],
            "overall_risk_score": self.overall_risk_score,
            "language": self.language,
            "checked_categories": self.checked_categories,
        }


DEFAULT_CATEGORIES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]

DEFAULT_THRESHOLD = 0.7


def check_single_text_safety(
    text: str,
    language: str = "en",
    categories: Optional[List[str]] = None,
    threshold: float = DEFAULT_THRESHOLD,
) -> SafetyCheckResult:
    """Check a single text for unsafe content using Perspective API.

    Args:
        text: Text to analyze.
        language: Language code of the text.
        categories: List of toxicity categories to check.
        threshold: Score threshold for flagging violations.

    Returns:
        SafetyCheckResult with violation details.
    """
    config = load_translation_config()
    api_key = os.environ.get("PERSPECTIVE_API_KEY", config.get("perspective_api_key"))

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable or config is required")

    check_categories = categories or DEFAULT_CATEGORIES

    requested_attributes = {cat: {} for cat in check_categories}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": [language],
        "spanAnnotations": True,
    }

    response = requests.post(
        f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=payload,
    )
    response.raise_for_status()

    result_data = response.json()
    attribute_scores = result_data.get("attributeScores", {})

    violations = []
    max_score = 0.0

    for category, scores in attribute_scores.items():
        summary_score = scores.get("summaryScore", {}).get("value", 0.0)
        max_score = max(max_score, summary_score)

        violation = SafetyViolation(
            category=category,
            score=round(summary_score, 4),
            threshold=threshold,
            text_segment=text[:200],
            is_violation=summary_score >= threshold,
        )
        violations.append(violation)

    return SafetyCheckResult(
        text=text[:500],
        is_safe=max_score < threshold,
        violations=violations,
        overall_risk_score=round(max_score, 4),
        language=language,
        checked_categories=check_categories,
    )


def check_localized_copy_safety(
    translations: List[Dict[str, str]],
    target_lang: str,
    categories: Optional[List[str]] = None,
    threshold: float = DEFAULT_THRESHOLD,
) -> List[SafetyCheckResult]:
    """Check multiple translated texts for unsafe content.

    Args:
        translations: List of dicts with 'text' and optionally 'source' keys.
        target_lang: Target language code.
        categories: Categories to check.
        threshold: Violation threshold.

    Returns:
        List of SafetyCheckResult objects.
    """
    results = []

    for trans in translations:
        text = trans.get("text", trans.get("translated", ""))
        if text:
            result = check_single_text_safety(
                text=text,
                language=target_lang,
                categories=categories,
                threshold=threshold,
            )
            results.append(result)

    return results


def generate_safety_report(results: List[SafetyCheckResult]) -> Dict[str, Any]:
    """Generate a summary report of safety checks.

    Args:
        results: List of SafetyCheckResult objects.

    Returns:
        Dictionary with safety report summary.
    """
    total_checked = len(results)
    total_violations = sum(1 for r in results if not r.is_safe)
    safe_count = total_checked - total_violations

    category_violations = {}
    for result in results:
        for violation in result.violations:
            if violation.is_violation:
                category_violations[violation.category] = (
                    category_violations.get(violation.category, 0) + 1
                )

    return {
        "total_texts_checked": total_checked,
        "safe_texts": safe_count,
        "flagged_texts": total_violations,
        "safety_rate": round(safe_count / total_checked, 3) if total_checked > 0 else 0,
        "violations_by_category": category_violations,
        "highest_risk_texts": sorted(
            [{"text": r.text, "risk_score": r.overall_risk_score} for r in results],
            key=lambda x: x["risk_score"],
            reverse=True,
        )[:5],
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        lang = sys.argv[1]
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if text:
            result = check_single_text_safety(text, lang)
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            print("Usage: unsafe_copy_check.py <language> <text>")
    else:
        print("Usage: unsafe_copy_check.py <language> <text>")

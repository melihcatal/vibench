"""Check platform model output for unsafe content.

Uses Amazon Comprehend DetectToxicContent API to analyze text output from
platform models for toxic or unsafe content categories including hate speech,
insults, sexual content, and violence.

Provider: Amazon Comprehend (part of AWS AI services)
SDK: boto3 (comprehend client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from typing import Any, Dict, List, Optional

from model_client import create_comprehend_client, resolve_bedrock_credentials
from model_models import SafetyCheckResult, build_safety_payload


TOXICITY_THRESHOLD = 0.5

TOXICITY_LABEL_MAP = {
    "HATE_SPEECH": "Hate speech or discriminatory language",
    "INSULT": "Insulting or demeaning language",
    "SEXUAL": "Sexually suggestive or explicit content",
    "VIOLENCE": "Violent or threatening content",
    "DRUGS": "References to illegal drugs or substances",
    "SELF_HARM": "Self-harm or suicide references",
    "PROFANITY": "Profane or vulgar language",
}


def check_output_safety(
    text: str,
    language_code: str = "en",
    threshold: float = TOXICITY_THRESHOLD,
) -> SafetyCheckResult:
    """Analyze platform model output for unsafe content using Amazon Comprehend.

    Args:
        text: Text output from the platform model to analyze.
        language_code: Language code for the text (default 'en').
        threshold: Confidence threshold for flagging content (0.0 to 1.0).

    Returns:
        SafetyCheckResult with safety assessment, flags, and scores.

    Raises:
        ValueError: If text is empty or too long.
        Exception: If Comprehend API call fails.
    """
    if not text or not text.strip():
        return SafetyCheckResult(is_safe=True)

    if len(text) > 5000:
        raise ValueError("Text exceeds Amazon Comprehend 5000 character limit")

    credentials = resolve_bedrock_credentials()
    client = create_comprehend_client(credentials)

    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode=language_code,
    )

    result_list = response.get("ResultList", [])
    if not result_list:
        return SafetyCheckResult(is_safe=True)

    labels = result_list[0].get("Labels", [])
    flags = []
    scores = {}

    for label in labels:
        name = label.get("Name", "")
        score = label.get("Score", 0.0)
        scores[name] = score

        if score >= threshold:
            description = TOXICITY_LABEL_MAP.get(name, name)
            flags.append(description)

    is_safe = len(flags) == 0

    return SafetyCheckResult(
        is_safe=is_safe,
        flags=flags,
        scores=scores,
        raw_response=response,
    )


def classify_content_severity(
    safety_result: SafetyCheckResult,
) -> str:
    """Classify the severity of unsafe content based on safety analysis.

    Args:
        safety_result: Result from check_output_safety.

    Returns:
        Severity level: 'safe', 'low', 'medium', 'high', or 'critical'.
    """
    if safety_result.is_safe:
        return "safe"

    max_score = max(safety_result.scores.values()) if safety_result.scores else 0.0
    num_flags = len(safety_result.flags)

    if max_score >= 0.9 or num_flags >= 3:
        return "critical"
    elif max_score >= 0.75:
        return "high"
    elif max_score >= 0.6:
        return "medium"
    else:
        return "low"


def generate_safety_report(
    text: str,
    safety_result: SafetyCheckResult,
) -> Dict[str, Any]:
    """Generate a detailed safety report for platform model output.

    Args:
        text: Original text analyzed.
        safety_result: Result from check_output_safety.

    Returns:
        Dict containing comprehensive safety assessment.
    """
    severity = classify_content_severity(safety_result)

    report = {
        "text_preview": text[:200] + ("..." if len(text) > 200 else ""),
        "text_length": len(text),
        "is_safe": safety_result.is_safe,
        "severity": severity,
        "flags": safety_result.flags,
        "detailed_scores": {
            k: round(v, 4) for k, v in safety_result.scores.items()
        },
        "recommendation": _get_recommendation(severity),
        "provider": "Amazon Comprehend",
        "api": "DetectToxicContent",
    }

    return report


def _get_recommendation(severity: str) -> str:
    """Get recommendation based on severity level."""
    recommendations = {
        "safe": "Content is safe for general audiences.",
        "low": "Minor concerns detected. Review recommended.",
        "medium": "Moderate concerns detected. Content review required.",
        "high": "Significant unsafe content detected. Do not distribute without review.",
        "critical": "Highly unsafe content detected. Block distribution immediately.",
    }
    return recommendations.get(severity, "Unknown severity level.")


if __name__ == "__main__":
    test_text = "This is a harmless test message."
    result = check_output_safety(test_text)
    report = generate_safety_report(test_text, result)
    print(report)

import os
import re
from typing import Dict, List, Any
from google.cloud import language_v1


def check_metric_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    """Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=annotation_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    safety_categories = []

    try:
        analyze_sentiment_response = client.analyze_sentiment(
            request={"document": document}
        )
        sentiment_score = analyze_sentiment_response.document_sentiment.score
        sentiment_magnitude = analyze_sentiment_response.document_sentiment.magnitude
    except Exception as e:
        sentiment_score = 0.0
        sentiment_magnitude = 0.0

    try:
        classify_text_response = client.classify_text(request={"document": document})
        categories = [category.name for category in classify_text_response.categories]
    except Exception as e:
        categories = []

    unsafe_patterns = [
        (r"\b(password|secret|key|token|credential)\b", "sensitive_info", "high"),
        (r"\b(attack|hack|exploit|breach)\b", "security_threat", "high"),
        (r"\b(down|outage|failure|error|crash)\b", "system_issue", "medium"),
        (r"\@\w+", "user_mention", "low"),
        (r"http[s]?://", "url_reference", "low"),
        (r"\b(PII|personally identifiable information)\b", "pii_reference", "high"),
        (r"\b(SSN|social security|credit card)\b", "pii_direct", "critical"),
    ]

    pattern_matches = []
    for pattern, category, severity in unsafe_patterns:
        matches = re.findall(pattern, annotation_text, re.IGNORECASE)
        if matches:
            pattern_matches.append(
                {
                    "pattern": pattern,
                    "category": category,
                    "severity": severity,
                    "matches": list(set(matches))[:5],
                }
            )

    contains_profanity = False
    profanity_patterns = [r"\b(shit|fuck|damn|hell|ass)\b", r"\b(crap|bitch|bastard)\b"]

    for pattern in profanity_patterns:
        if re.search(pattern, annotation_text, re.IGNORECASE):
            contains_profanity = True
            break

    sentiment_risk = "low"
    if sentiment_score < -0.5:
        sentiment_risk = "high"
    elif sentiment_score < -0.2:
        sentiment_risk = "medium"

    overall_risk = "low"
    if any(match["severity"] == "critical" for match in pattern_matches):
        overall_risk = "critical"
    elif any(match["severity"] == "high" for match in pattern_matches):
        overall_risk = "high"
    elif contains_profanity:
        overall_risk = "medium"
    elif sentiment_risk == "high":
        overall_risk = "medium"
    elif any(match["severity"] == "medium" for match in pattern_matches):
        overall_risk = "medium"

    safety_result = {
        "annotation_text": annotation_text,
        "safety_check": {
            "overall_risk": overall_risk,
            "sentiment_analysis": {
                "score": sentiment_score,
                "magnitude": sentiment_magnitude,
                "risk_level": sentiment_risk,
            },
            "contains_profanity": contains_profanity,
            "pattern_matches": pattern_matches,
            "detected_categories": categories[:5],
        },
        "recommendations": [],
    }

    if overall_risk == "critical":
        safety_result["recommendations"].append(
            "DO NOT USE: Contains critical security risks"
        )
    elif overall_risk == "high":
        safety_result["recommendations"].append(
            "Review required: Contains high-risk patterns"
        )
    elif overall_risk == "medium":
        safety_result["recommendations"].append(
            "Consider revising: Contains medium-risk content"
        )

    if contains_profanity:
        safety_result["recommendations"].append("Remove profanity from annotation")

    if any("pii" in match["category"] for match in pattern_matches):
        safety_result["recommendations"].append(
            "Remove PII references from metric annotation"
        )

    if sentiment_risk in ["high", "medium"]:
        safety_result["recommendations"].append(
            "Consider using neutral language for metric annotations"
        )

    return safety_result

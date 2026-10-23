import os
import re
from typing import Dict, List, Optional
from google.cloud import language_v1


def check_annotation_safety(text: str, check_types: List[str] = None) -> Dict[str, Any]:
    """
    Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API.

    Args:
        text: The text to analyze for safety
        check_types: Types of safety checks to perform (default: all)

    Returns:
        Dictionary with safety analysis results
    """
    if check_types is None:
        check_types = [
            "toxicity",
            "profanity",
            "insult",
            "threat",
            "sexual",
            "flirtation",
        ]

    client = language_v1.LanguageServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
    )

    try:
        response = client.analyze_sentiment(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude

    except Exception as e:
        sentiment_score = 0.0
        sentiment_magnitude = 0.0

    try:
        response = client.classify_text(
            request={
                "document": document,
                "classification_model_options": {
                    "v2_model": {
                        "content_categories_version": language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
                    }
                },
            }
        )

        categories = []
        for category in response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

    except Exception as e:
        categories = []

    unsafe_patterns = [
        (
            r"\b(pass(word|wd|phrase)?|secret|key|token|auth|credential)\b",
            "sensitive_info",
        ),
        (r"\b(admin|root|sudo|privilege|escalation)\b", "privilege_reference"),
        (r"\b(attack|exploit|vulnerability|breach|hack)\b", "security_threat"),
        (r"\b(error|fail(ure)?|crash|down|outage)\b", "negative_terminology"),
        (r"(\d{1,3}\.){3}\d{1,3}", "ip_address"),
        (r"[a-fA-F0-9]{32,}", "hash_like"),
        (r"[\w\.]+@[\w\.]+\.\w+", "email_address"),
        (r"https?://[^\s]+", "url_reference"),
    ]

    pattern_matches = []
    for pattern, label in unsafe_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            pattern_matches.append(
                {
                    "pattern": label,
                    "matches": list(set(matches))[:5],
                    "count": len(matches),
                }
            )

    toxicity_keywords = [
        "hate",
        "racist",
        "sexist",
        "offensive",
        "abusive",
        "violent",
        "threat",
        "kill",
        "harm",
        "attack",
    ]

    toxicity_matches = []
    for keyword in toxicity_keywords:
        if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
            toxicity_matches.append(keyword)

    profanity_list = [
        "fuck",
        "shit",
        "ass",
        "bitch",
        "damn",
        "hell",
        "crap",
        "piss",
        "dick",
        "cock",
        "pussy",
        "cunt",
    ]

    profanity_matches = []
    for word in profanity_list:
        if re.search(rf"\b{word}\b", text, re.IGNORECASE):
            profanity_matches.append(word)

    safety_score = 1.0

    if sentiment_score < -0.5:
        safety_score *= 0.8

    if toxicity_matches:
        safety_score *= 0.7

    if profanity_matches:
        safety_score *= 0.6

    if pattern_matches:
        safety_score *= 0.9

    high_risk_categories = ["/Law & Government", "/News", "/Sensitive Subjects"]
    for category in categories:
        if category["name"] in high_risk_categories and category["confidence"] > 0.7:
            safety_score *= 0.8

    is_safe = safety_score > 0.6

    result = {
        "text": text,
        "is_safe": is_safe,
        "safety_score": safety_score,
        "sentiment": {
            "score": sentiment_score,
            "magnitude": sentiment_magnitude,
            "label": "positive"
            if sentiment_score > 0.1
            else "negative"
            if sentiment_score < -0.1
            else "neutral",
        },
        "categories": categories[:3],
        "pattern_matches": pattern_matches,
        "toxicity_matches": toxicity_matches,
        "profanity_matches": profanity_matches,
        "recommendations": [],
    }

    if not is_safe:
        result["recommendations"].append(
            "Consider revising or removing this annotation"
        )

    if toxicity_matches:
        result["recommendations"].append(
            f"Contains potentially toxic language: {', '.join(toxicity_matches)}"
        )

    if profanity_matches:
        result["recommendations"].append(
            f"Contains profanity: {', '.join(profanity_matches)}"
        )

    if pattern_matches:
        sensitive_patterns = [
            p
            for p in pattern_matches
            if p["pattern"] in ["sensitive_info", "ip_address", "email_address"]
        ]
        if sensitive_patterns:
            result["recommendations"].append(
                "Contains potentially sensitive information"
            )

    return result


if __name__ == "__main__":
    test_annotations = [
        "CPU utilization is normal",
        "System error: authentication failure for user admin",
        "High memory usage detected on server 192.168.1.1",
        "This is fucking terrible performance",
        "Potential security vulnerability detected",
    ]

    for annotation in test_annotations:
        try:
            safety_check = check_annotation_safety(annotation)
            print(f"Annotation: {annotation[:50]}...")
            print(f"  Safe: {safety_check['is_safe']}")
            print(f"  Score: {safety_check['safety_score']:.2f}")
            print(f"  Sentiment: {safety_check['sentiment']['label']}")
            if safety_check["recommendations"]:
                print(f"  Recommendations: {safety_check['recommendations'][0]}")
            print()
        except Exception as e:
            print(f"Error checking annotation safety: {e}")

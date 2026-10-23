import os
from typing import Dict, Any, List, Optional
import re
from google.cloud import language_v1
import google.api_core.exceptions
from openai import OpenAI


def check_annotation_safety(text: str, check_types: List[str] = None) -> Dict[str, Any]:
    """
    Check free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API.

    Args:
        text: Text to check for safety
        check_types: Types of checks to perform (toxicity, profanity, hate_speech, etc.)

    Returns:
        Dictionary containing safety analysis results
    """
    if check_types is None:
        check_types = ["toxicity", "profanity", "hate_speech", "insult", "threat"]

    try:
        client = language_v1.LanguageServiceClient()

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        features = language_v1.AnnotateTextRequest.Features(
            extract_entities=True, extract_document_sentiment=True, classify_text=False
        )

        response = client.annotate_text(
            request={
                "document": document,
                "features": features,
            }
        )

        safety_analysis = analyze_text_safety(text, response, check_types)

        openai_analysis = (
            check_with_openai(text) if os.environ.get("OPENAI_API_KEY") else None
        )

        combined_analysis = combine_safety_analyses(safety_analysis, openai_analysis)

        return {
            "text": text,
            "text_length": len(text),
            "safety_analysis": combined_analysis,
            "is_safe": combined_analysis.get("overall_safe", True),
            "recommendations": generate_safety_recommendations(combined_analysis),
        }

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Natural Language API error: {e}")
        return fallback_safety_check(text, check_types)
    except Exception as e:
        print(f"Error checking annotation safety: {e}")
        return fallback_safety_check(text, check_types)


def analyze_text_safety(
    text: str, language_response: Any, check_types: List[str]
) -> Dict[str, Any]:
    """
    Analyze text safety using Google Cloud Natural Language API response.

    Args:
        text: Original text
        language_response: Response from Google Cloud Natural Language API
        check_types: Types of checks to perform

    Returns:
        Safety analysis results
    """
    analysis = {
        "overall_safe": True,
        "checks": {},
        "entities": [],
        "sentiment": {},
        "red_flags": [],
    }

    if hasattr(language_response, "entities"):
        for entity in language_response.entities:
            entity_info = {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": [
                    {"text": m.text.content, "type": m.type_.name}
                    for m in entity.mentions
                ],
            }
            analysis["entities"].append(entity_info)

            if entity.type_ in [
                language_v1.Entity.Type.PERSON,
                language_v1.Entity.Type.LOCATION,
            ]:
                analysis["red_flags"].append(
                    f"Contains {entity.type_.name.lower()}: {entity.name}"
                )

    if hasattr(language_response, "document_sentiment"):
        sentiment = language_response.document_sentiment
        analysis["sentiment"] = {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
            "label": "positive"
            if sentiment.score > 0.25
            else "negative"
            if sentiment.score < -0.25
            else "neutral",
        }

        if sentiment.score < -0.5 and sentiment.magnitude > 0.5:
            analysis["red_flags"].append("Strong negative sentiment detected")
            analysis["overall_safe"] = False

    for check_type in check_types:
        check_result = perform_specific_check(text, check_type)
        analysis["checks"][check_type] = check_result

        if not check_result.get("safe", True):
            analysis["overall_safe"] = False

    pattern_checks = perform_pattern_checks(text)
    analysis["pattern_checks"] = pattern_checks

    for pattern, result in pattern_checks.items():
        if not result.get("safe", True):
            analysis["red_flags"].append(f"Pattern check failed: {pattern}")
            analysis["overall_safe"] = False

    return analysis


def perform_specific_check(text: str, check_type: str) -> Dict[str, Any]:
    """
    Perform specific safety check on text.

    Args:
        text: Text to check
        check_type: Type of check to perform

    Returns:
        Check results
    """
    text_lower = text.lower()

    if check_type == "profanity":
        profanity_patterns = [
            r"\b(fuck|shit|damn|hell|bitch|asshole|bastard|cunt)\b",
            r"\b(nigger|nigga|chink|spic|kike|gook)\b",
        ]

        matches = []
        for pattern in profanity_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)

        return {
            "safe": len(matches) == 0,
            "matches": matches,
            "confidence": 0.8 if matches else 0.2,
        }

    elif check_type == "hate_speech":
        hate_keywords = [
            "kill all",
            "exterminate",
            "purge",
            "ethnic cleansing",
            "superior race",
            "inferior race",
            "racial purity",
        ]

        matches = [kw for kw in hate_keywords if kw in text_lower]

        return {
            "safe": len(matches) == 0,
            "matches": matches,
            "confidence": 0.9 if matches else 0.1,
        }

    elif check_type == "threat":
        threat_patterns = [
            r"\b(kill|murder|assassinate|bomb|shoot|stab|attack)\s+(you|them|us|everyone)\b",
            r"\b(threat|threaten|harm|hurt|destroy)\s+(you|your|them|their)\b",
            r"\b(die|death|dead)\s+(wish|hope|want)\b",
        ]

        matches = []
        for pattern in threat_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)

        return {
            "safe": len(matches) == 0,
            "matches": matches,
            "confidence": 0.85 if matches else 0.15,
        }

    elif check_type == "insult":
        insult_patterns = [
            r"\b(stupid|idiot|moron|retard|dumb|fool)\b",
            r"\b(worthless|useless|pathetic|loser|failure)\b",
            r"\b(hate|despise|loathe)\s+(you|them)\b",
        ]

        matches = []
        for pattern in insult_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)

        return {
            "safe": len(matches) == 0,
            "matches": matches,
            "confidence": 0.7 if matches else 0.3,
        }

    elif check_type == "toxicity":
        toxic_patterns = [
            r"\b(disgusting|revolting|vile|filthy|rotten)\b",
            r"\b(cancer|disease|plague|infection)\s+(of|to)\b",
            r"\b(should die|deserve to die|burn in hell)\b",
        ]

        matches = []
        for pattern in toxic_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)

        return {
            "safe": len(matches) == 0,
            "matches": matches,
            "confidence": 0.75 if matches else 0.25,
        }

    return {"safe": True, "matches": [], "confidence": 0.5}


def perform_pattern_checks(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Perform pattern-based checks on text.

    Args:
        text: Text to check

    Returns:
        Pattern check results
    """
    checks = {}

    url_pattern = r"https?://[^\s]+"
    url_matches = re.findall(url_pattern, text)
    checks["urls"] = {
        "safe": len(url_matches) == 0,
        "matches": url_matches,
        "count": len(url_matches),
    }

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    email_matches = re.findall(email_pattern, text)
    checks["emails"] = {
        "safe": len(email_matches) == 0,
        "matches": email_matches,
        "count": len(email_matches),
    }

    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ip_matches = re.findall(ip_pattern, text)
    checks["ip_addresses"] = {
        "safe": len(ip_matches) == 0,
        "matches": ip_matches,
        "count": len(ip_matches),
    }

    secret_pattern = (
        r"\b(api[_-]?key|secret[_-]?key|password|token|credential)\s*[:=]\s*[\w\-]+\b"
    )
    secret_matches = re.findall(secret_pattern, text, re.IGNORECASE)
    checks["secrets"] = {
        "safe": len(secret_matches) == 0,
        "matches": secret_matches,
        "count": len(secret_matches),
    }

    return checks


def check_with_openai(text: str) -> Optional[Dict[str, Any]]:
    """
    Check text safety using OpenAI moderation API.

    Args:
        text: Text to check

    Returns:
        OpenAI moderation results or None
    """
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.moderations.create(model="text-moderation-latest", input=text)

        result = response.results[0]

        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
            "openai_model": "text-moderation-latest",
        }

    except Exception as e:
        print(f"OpenAI moderation check failed: {e}")
        return None


def combine_safety_analyses(
    google_analysis: Dict[str, Any], openai_analysis: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Combine safety analyses from multiple sources.

    Args:
        google_analysis: Analysis from Google Cloud Natural Language
        openai_analysis: Analysis from OpenAI moderation

    Returns:
        Combined analysis
    """
    combined = google_analysis.copy()

    if openai_analysis:
        combined["openai_analysis"] = openai_analysis

        if openai_analysis.get("flagged", False):
            combined["overall_safe"] = False

            flagged_categories = [
                cat
                for cat, flagged in openai_analysis.get("categories", {}).items()
                if flagged
            ]

            if flagged_categories:
                combined["red_flags"].append(
                    f"OpenAI flagged categories: {', '.join(flagged_categories)}"
                )

    return combined


def generate_safety_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """
    Generate safety recommendations based on analysis.

    Args:
        analysis: Safety analysis results

    Returns:
        List of recommendations
    """
    recommendations = []

    if not analysis.get("overall_safe", True):
        recommendations.append(
            "Text contains unsafe content - consider revising or removing"
        )

    red_flags = analysis.get("red_flags", [])
    if red_flags:
        recommendations.append(f"Review {len(red_flags)} red flag(s) identified")

    pattern_checks = analysis.get("pattern_checks", {})
    if pattern_checks.get("urls", {}).get("count", 0) > 0:
        recommendations.append("Remove URLs from metric annotations")

    if pattern_checks.get("emails", {}).get("count", 0) > 0:
        recommendations.append("Remove email addresses from metric annotations")

    if pattern_checks.get("secrets", {}).get("count", 0) > 0:
        recommendations.append("Potential secrets detected - review immediately")

    sentiment = analysis.get("sentiment", {}).get("label", "neutral")
    if sentiment == "negative":
        recommendations.append(
            "Consider using neutral or positive language for metric annotations"
        )

    return recommendations


def fallback_safety_check(text: str, check_types: List[str]) -> Dict[str, Any]:
    """
    Fallback safety check when API calls fail.

    Args:
        text: Text to check
        check_types: Types of checks to perform

    Returns:
        Basic safety analysis
    """
    analysis = {
        "overall_safe": True,
        "checks": {},
        "red_flags": [],
        "pattern_checks": perform_pattern_checks(text),
    }

    for check_type in check_types:
        check_result = perform_specific_check(text, check_type)
        analysis["checks"][check_type] = check_result

        if not check_result.get("safe", True):
            analysis["overall_safe"] = False
            analysis["red_flags"].append(f"{check_type} check failed")

    return {
        "text": text,
        "text_length": len(text),
        "safety_analysis": analysis,
        "is_safe": analysis["overall_safe"],
        "recommendations": generate_safety_recommendations(analysis),
        "note": "Using fallback checks (API unavailable)",
    }

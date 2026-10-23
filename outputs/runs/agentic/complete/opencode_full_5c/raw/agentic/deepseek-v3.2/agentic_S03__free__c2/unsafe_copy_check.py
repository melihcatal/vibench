import os
from typing import Dict, List, Any
from translation_client import TranslationClient


def unsafe_copy_check(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Google Cloud Perspective API.

    Args:
        text: Text to check for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety scores and flagged attributes
    """
    client = TranslationClient()

    # Use Google Cloud Perspective API for content safety checking
    # Note: This requires the google-cloud-language package and Perspective API setup

    try:
        # Import Perspective API client
        from googleapiclient import discovery
        import json

        # Initialize Perspective API client
        # In production, you would use proper API key management
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

        if not api_key:
            # Fallback to basic checks if API key not available
            return basic_safety_check(text, language_code)

        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        analyze_request = {
            "comment": {"text": text},
            "languages": [language_code],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
                "FLIRTATION": {},
            },
        }

        response = client.comments().analyze(body=analyze_request).execute()

        # Extract scores
        scores = {}
        flagged_attributes = []

        for attr_name, attr_data in response.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            scores[attr_name.lower()] = score

            if score > 0.7:  # Threshold for flagging
                flagged_attributes.append(attr_name.lower())

        return {
            "text": text,
            "language": language_code,
            "safety_scores": scores,
            "flagged_attributes": flagged_attributes,
            "is_safe": len(flagged_attributes) == 0,
            "provider": "google-perspective-api",
        }

    except ImportError:
        # Fallback if Perspective API not available
        return basic_safety_check(text, language_code)
    except Exception as e:
        # Fallback on any error
        print(f"Perspective API error: {e}")
        return basic_safety_check(text, language_code)


def basic_safety_check(text: str, language_code: str) -> Dict[str, Any]:
    """Basic safety check as fallback."""
    # Simple keyword-based check
    unsafe_keywords = {
        "en": ["hate", "kill", "attack", "violence", "abuse", "threat"],
        "es": ["odio", "matar", "ataque", "violencia", "abuso", "amenaza"],
        "fr": ["haine", "tuer", "attaque", "violence", "abus", "menace"],
    }

    keywords = unsafe_keywords.get(language_code, unsafe_keywords["en"])
    text_lower = text.lower()

    found_keywords = []
    for keyword in keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)

    return {
        "text": text,
        "language": language_code,
        "safety_scores": {"basic_check": 1.0 if found_keywords else 0.0},
        "flagged_attributes": ["unsafe_keywords"] if found_keywords else [],
        "is_safe": len(found_keywords) == 0,
        "provider": "basic-keyword-check",
        "found_keywords": found_keywords,
    }

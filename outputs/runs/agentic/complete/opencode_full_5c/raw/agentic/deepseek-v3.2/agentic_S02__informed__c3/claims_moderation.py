import os
import json
from typing import Dict, Any, List
import requests


def moderate_user_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    text_to_analyze = extract_text_from_claims(claims)

    if not text_to_analyze:
        return {
            "moderated": False,
            "reason": "No text content to moderate",
            "claims": claims,
        }

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text_to_analyze},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    params = {"key": api_key}

    try:
        response = requests.post(api_url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        moderation_scores = {}
        for attr_name, attr_data in result.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            moderation_scores[attr_name.lower()] = score

        is_flagged = any(score > 0.7 for score in moderation_scores.values())

        moderation_result = {
            "moderated": True,
            "flagged": is_flagged,
            "scores": moderation_scores,
            "original_claims": claims,
            "perspective_api_used": True,
        }

        if is_flagged:
            high_risk_attributes = [
                attr for attr, score in moderation_scores.items() if score > 0.7
            ]
            moderation_result["high_risk_attributes"] = high_risk_attributes
            moderation_result["action"] = "REVIEW_REQUIRED"
        else:
            moderation_result["action"] = "APPROVED"

        return moderation_result

    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API request failed: {e}")


def extract_text_from_claims(claims: Dict[str, Any]) -> str:
    text_fields = []

    text_fields.append(claims.get("name", ""))
    text_fields.append(claims.get("nickname", ""))
    text_fields.append(claims.get("given_name", ""))
    text_fields.append(claims.get("family_name", ""))

    if "custom_claims" in claims and isinstance(claims["custom_claims"], dict):
        for key, value in claims["custom_claims"].items():
            if isinstance(value, str):
                text_fields.append(value)

    non_empty_text = [
        field for field in text_fields if field and isinstance(field, str)
    ]

    return " ".join(non_empty_text)


def batch_moderate_claims(claims_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    results = []

    for claims in claims_list:
        try:
            moderation_result = moderate_user_claims(claims)
            results.append(moderation_result)
        except Exception as e:
            results.append({"moderated": False, "error": str(e), "claims": claims})

    return results


def check_claim_safety(claims: Dict[str, Any], threshold: float = 0.7) -> bool:
    moderation_result = moderate_user_claims(claims)

    if not moderation_result.get("moderated", False):
        return True

    if moderation_result.get("flagged", False):
        return False

    scores = moderation_result.get("scores", {})
    for score in scores.values():
        if score > threshold:
            return False

    return True

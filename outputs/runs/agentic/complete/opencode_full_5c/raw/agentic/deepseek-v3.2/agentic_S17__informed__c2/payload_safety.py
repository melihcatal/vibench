import os
import json
from typing import Dict, Any, List
import requests
from security_models import DecryptionResponse


def check_payload_safety(decrypted_response: DecryptionResponse) -> Dict[str, Any]:
    """
    Check decrypted text payloads for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    if not decrypted_response.success or not decrypted_response.plaintext:
        return {
            "safe": False,
            "error": "No decrypted plaintext available",
            "provider": "perspective-api",
        }

    text = decrypted_response.plaintext

    # Prepare request for Perspective API
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Define attributes to check
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"],
        "doNotStore": True,
    }

    headers = {"Content-Type": "application/json"}

    params = {"key": api_key}

    try:
        response = requests.post(url, params=params, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract attribute scores
        attribute_scores = {}
        for attr_name, attr_data in result.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            attribute_scores[attr_name] = round(score, 4)

        # Determine if content is safe based on thresholds
        # Common threshold: 0.7 for high confidence of toxicity
        toxicity_threshold = 0.7
        severe_toxicity_threshold = 0.8

        is_safe = True
        unsafe_attributes = []

        for attr_name, score in attribute_scores.items():
            if attr_name == "TOXICITY" and score > toxicity_threshold:
                is_safe = False
                unsafe_attributes.append(f"{attr_name}: {score}")
            elif attr_name == "SEVERE_TOXICITY" and score > severe_toxicity_threshold:
                is_safe = False
                unsafe_attributes.append(f"{attr_name}: {score}")
            elif (
                attr_name in ["IDENTITY_ATTACK", "THREAT", "SEXUALLY_EXPLICIT"]
                and score > 0.8
            ):
                is_safe = False
                unsafe_attributes.append(f"{attr_name}: {score}")
            elif attr_name in ["INSULT", "PROFANITY"] and score > 0.9:
                is_safe = False
                unsafe_attributes.append(f"{attr_name}: {score}")

        return {
            "safe": is_safe,
            "attribute_scores": attribute_scores,
            "unsafe_attributes": unsafe_attributes if not is_safe else [],
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "provider": "perspective-api",
            "key_id": decrypted_response.key_id,
            "timestamp": decrypted_response.timestamp.isoformat()
            if decrypted_response.timestamp
            else None,
        }

    except requests.exceptions.RequestException as e:
        return {
            "safe": False,
            "error": f"API request failed: {str(e)}",
            "provider": "perspective-api",
        }
    except Exception as e:
        return {"safe": False, "error": str(e), "provider": "perspective-api"}

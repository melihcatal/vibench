import os
import json
from typing import Dict, Any, List
import requests


def check_labels_safety(
    labels: List[Dict[str, Any]], api_key: str = None
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    label_texts = [
        label.get("description", "") for label in labels if label.get("description")
    ]
    combined_text = " ".join(label_texts)

    if not combined_text:
        return {"is_safe": True, "scores": {}, "error": "No text to analyze"}

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": combined_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=data)

    if response.status_code != 200:
        return {
            "is_safe": False,
            "scores": {},
            "error": f"API error: {response.status_code}",
        }

    result = response.json()

    attribute_scores = result.get("attributeScores", {})
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        scores[attr_name] = attr_data.get("summaryScore", {}).get("value", 0)

    is_safe = all(score < 0.7 for score in scores.values())

    return {"is_safe": is_safe, "scores": scores, "attribute_scores": attribute_scores}


def check_description_safety(description: str, api_key: str = None) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not description:
        return {"is_safe": True, "scores": {}, "error": "No description to analyze"}

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": description},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=data)

    if response.status_code != 200:
        return {
            "is_safe": False,
            "scores": {},
            "error": f"API error: {response.status_code}",
        }

    result = response.json()

    attribute_scores = result.get("attributeScores", {})
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        scores[attr_name] = attr_data.get("summaryScore", {}).get("value", 0)

    is_safe = all(score < 0.7 for score in scores.values())

    return {"is_safe": is_safe, "scores": scores, "attribute_scores": attribute_scores}


def check_detected_text_safety(
    text_detection: Dict[str, Any], api_key: str = None
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    detected_text = text_detection.get("full_text", "")

    if not detected_text:
        return {"is_safe": True, "scores": {}, "error": "No detected text to analyze"}

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": detected_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=data)

    if response.status_code != 200:
        return {
            "is_safe": False,
            "scores": {},
            "error": f"API error: {response.status_code}",
        }

    result = response.json()

    attribute_scores = result.get("attributeScores", {})
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        scores[attr_name] = attr_data.get("summaryScore", {}).get("value", 0)

    is_safe = all(score < 0.7 for score in scores.values())

    return {"is_safe": is_safe, "scores": scores, "attribute_scores": attribute_scores}

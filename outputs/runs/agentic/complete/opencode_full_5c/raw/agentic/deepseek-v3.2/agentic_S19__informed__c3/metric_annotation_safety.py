import os
import requests
from typing import Dict, Any, List


def check_metric_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": annotation_text},
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

    params = {"key": api_key}

    try:
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()
        result = response.json()

        scores = {}
        for attribute_name, attribute_data in result.get("attributeScores", {}).items():
            scores[attribute_name.lower()] = attribute_data.get("summaryScore", {}).get(
                "value", 0
            )

        is_safe = all(score < 0.7 for score in scores.values())

        return {
            "is_safe": is_safe,
            "scores": scores,
            "flagged_attributes": [
                attr for attr, score in scores.items() if score >= 0.7
            ],
            "highest_score": max(scores.values()) if scores else 0,
        }
    except requests.exceptions.RequestException as e:
        return {
            "is_safe": False,
            "error": str(e),
            "scores": {},
            "flagged_attributes": ["api_error"],
        }


def check_batch_metric_labels(labels: List[str]) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = {}
    for label in labels:
        payload = {
            "comment": {"text": label},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        }

        params = {"key": api_key}

        try:
            response = requests.post(url, json=payload, params=params)
            response.raise_for_status()
            result = response.json()

            toxicity_score = (
                result.get("attributeScores", {})
                .get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )
            severe_toxicity_score = (
                result.get("attributeScores", {})
                .get("SEVERE_TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0)
            )

            results[label] = {
                "is_safe": toxicity_score < 0.7 and severe_toxicity_score < 0.7,
                "toxicity_score": toxicity_score,
                "severe_toxicity_score": severe_toxicity_score,
            }
        except requests.exceptions.RequestException:
            results[label] = {
                "is_safe": False,
                "error": "API request failed",
                "toxicity_score": 1.0,
                "severe_toxicity_score": 1.0,
            }

    unsafe_labels = [
        label for label, result in results.items() if not result.get("is_safe", True)
    ]

    return {
        "results": results,
        "unsafe_labels": unsafe_labels,
        "total_checked": len(labels),
        "unsafe_count": len(unsafe_labels),
    }

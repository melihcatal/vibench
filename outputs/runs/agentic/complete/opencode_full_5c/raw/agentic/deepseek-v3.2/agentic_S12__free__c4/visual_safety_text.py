import os
from typing import List, Dict, Any
import requests


def check_labels_for_unsafe_text(labels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe text using Google Perspective API.

    Args:
        labels: List of label dictionaries with 'description' field

    Returns:
        Dictionary containing safety analysis results
    """
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    all_label_text = " ".join([label.get("description", "") for label in labels])

    params = {"key": api_key}

    data = {
        "comment": {"text": all_label_text},
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
        raise Exception(
            f"Google Perspective API error: {response.status_code} - {response.text}"
        )

    result = response.json()

    attribute_scores = result.get("attributeScores", {})

    safety_scores = {}
    for attr_name, attr_data in attribute_scores.items():
        safety_scores[attr_name.lower()] = {
            "score": attr_data.get("summaryScore", {}).get("value", 0.0),
            "threshold": 0.7,  # Common threshold for moderation
        }

    # Check if any score exceeds threshold
    unsafe_categories = []
    for attr_name, scores in safety_scores.items():
        if scores["score"] > scores["threshold"]:
            unsafe_categories.append(attr_name)

    return {
        "is_unsafe": len(unsafe_categories) > 0,
        "unsafe_categories": unsafe_categories,
        "safety_scores": safety_scores,
        "provider": "google-perspective-api",
        "total_labels_checked": len(labels),
        "label_text_sample": all_label_text[:100] + "..."
        if len(all_label_text) > 100
        else all_label_text,
    }


def check_individual_labels(labels: List[str]) -> List[Dict[str, Any]]:
    """
    Check individual labels for safety.

    Args:
        labels: List of label strings

    Returns:
        List of safety results for each label
    """
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}

    results = []

    for label in labels:
        data = {
            "comment": {"text": label},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }

        response = requests.post(url, params=params, json=data)

        if response.status_code == 200:
            result = response.json()
            score = (
                result.get("attributeScores", {})
                .get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0.0)
            )
            results.append(
                {
                    "label": label,
                    "toxicity_score": score,
                    "is_unsafe": score > 0.7,
                    "provider": "google-perspective-api",
                }
            )
        else:
            results.append(
                {
                    "label": label,
                    "error": f"API error: {response.status_code}",
                    "provider": "google-perspective-api",
                }
            )

    return results


if __name__ == "__main__":
    # Example usage
    sample_labels = [
        {"description": "sunset", "score": 0.95},
        {"description": "beach", "score": 0.92},
        {"description": "ocean", "score": 0.90},
    ]

    try:
        safety_check = check_labels_for_unsafe_text(sample_labels)
        print(f"Is unsafe: {safety_check['is_unsafe']}")
        print(f"Unsafe categories: {safety_check['unsafe_categories']}")
        print(f"Provider: {safety_check['provider']}")
        for attr, scores in safety_check["safety_scores"].items():
            print(f"{attr}: {scores['score']:.3f}")
    except Exception as e:
        print(f"Error: {e}")

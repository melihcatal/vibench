import os
from typing import Dict, Any, List
import requests


def visual_safety_text(labels: List[str], descriptions: List[str]) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe text using Perspective API.

    Args:
        labels: List of detected labels
        descriptions: List of image descriptions

    Returns:
        Dictionary containing safety analysis results
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    # Combine all text for analysis
    all_text = " ".join(labels + descriptions)

    if not all_text.strip():
        return {"is_safe": True, "scores": {}, "flagged_categories": []}

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    payload = {
        "comment": {"text": all_text},
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

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        scores = {}
        flagged_categories = []

        for attribute_name, attribute_data in data.get("attributeScores", {}).items():
            score = attribute_data.get("summaryScore", {}).get("value", 0)
            scores[attribute_name] = score

            if score > 0.7:  # Threshold for flagging
                flagged_categories.append(attribute_name)

        return {
            "is_safe": len(flagged_categories) == 0,
            "scores": scores,
            "flagged_categories": flagged_categories,
            "text_analyzed": all_text[:200] + "..."
            if len(all_text) > 200
            else all_text,
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Safety analysis failed: {str(e)}")

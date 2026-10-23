import os
import requests
from typing import Dict, List, Any, Optional


def secret_label_safety(
    secret_labels: Dict[str, str], api_key: str = None
) -> Dict[str, Any]:
    """Check secret labels and notes for unsafe text using Perspective API."""
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = {
        "total_labels": len(secret_labels),
        "unsafe_labels": 0,
        "label_details": [],
    }

    for label_name, label_value in secret_labels.items():
        if not label_value:
            continue

        payload = {
            "comment": {"text": label_value},
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
            response = requests.post(
                f"{api_url}?key={api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            analysis = response.json()
            attribute_scores = analysis.get("attributeScores", {})

            label_result = {
                "label_name": label_name,
                "label_value": label_value,
                "scores": {},
                "is_unsafe": False,
                "unsafe_attributes": [],
            }

            for attr_name, attr_data in attribute_scores.items():
                score = attr_data.get("summaryScore", {}).get("value", 0)
                label_result["scores"][attr_name] = score

                if score > 0.7:  # Threshold for unsafe content
                    label_result["is_unsafe"] = True
                    label_result["unsafe_attributes"].append(attr_name)

            if label_result["is_unsafe"]:
                results["unsafe_labels"] += 1

            results["label_details"].append(label_result)

        except requests.exceptions.RequestException as e:
            error_result = {
                "label_name": label_name,
                "label_value": label_value,
                "error": str(e),
                "is_unsafe": False,
                "scores": {},
            }
            results["label_details"].append(error_result)

    results["safety_percentage"] = (
        (
            (results["total_labels"] - results["unsafe_labels"])
            / results["total_labels"]
            * 100
        )
        if results["total_labels"] > 0
        else 100
    )

    return results

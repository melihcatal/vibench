import os
import requests
from typing import List, Dict, Any


def secret_label_safety(
    secret_labels: List[str], secret_notes: List[str]
) -> Dict[str, Any]:
    """
    Check secret labels and notes for unsafe text using Perspective API.

    Args:
        secret_labels: List of secret label strings
        secret_notes: List of secret note/description strings

    Returns:
        Dictionary with safety analysis results
    """
    # Perspective API provider-specific configuration
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    all_texts = secret_labels + secret_notes
    results = []

    for text in all_texts:
        if not text or not text.strip():
            continue

        # Prepare request for Perspective API
        request_data = {
            "comment": {"text": text},
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
                f"{api_url}?key={api_key}", json=request_data, timeout=10
            )
            response.raise_for_status()

            analysis = response.json()

            # Extract scores
            scores = {}
            for attribute_name, attribute_data in analysis.get(
                "attributeScores", {}
            ).items():
                scores[attribute_name.lower()] = attribute_data.get(
                    "summaryScore", {}
                ).get("value", 0)

            results.append(
                {
                    "text": text,
                    "scores": scores,
                    "is_label": text in secret_labels,
                    "is_note": text in secret_notes,
                }
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Perspective API request failed: {e}")
        except ValueError as e:
            raise RuntimeError(f"Invalid response from Perspective API: {e}")

    # Analyze results
    unsafe_items = []
    for result in results:
        # Check if any score exceeds threshold
        high_scores = {k: v for k, v in result["scores"].items() if v > 0.7}
        if high_scores:
            unsafe_items.append(
                {
                    "text": result["text"],
                    "high_scores": high_scores,
                    "type": "label" if result["is_label"] else "note",
                }
            )

    # Generate summary
    total_checked = len(results)
    total_unsafe = len(unsafe_items)

    summary = {
        "total_texts_checked": total_checked,
        "total_unsafe_found": total_unsafe,
        "unsafe_items": unsafe_items,
        "safety_score": 1.0 - (total_unsafe / max(total_checked, 1)),
        "provider": "Perspective API",
        "attributes_checked": [
            "toxicity",
            "severe_toxicity",
            "identity_attack",
            "insult",
            "profanity",
            "threat",
        ],
    }

    # Add recommendations
    if total_unsafe > 0:
        summary["recommendations"] = [
            "Review and clean unsafe secret labels/notes",
            "Consider using more neutral, descriptive language",
            "Avoid personal identifiers or sensitive information in labels",
        ]
    else:
        summary["recommendations"] = [
            "Secret labels and notes appear safe",
            "Continue current labeling practices",
        ]

    return summary

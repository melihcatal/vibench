import os
import requests
from typing import Dict, Any, List


def check_secret_labels_safety(secret_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check secret labels and notes for unsafe text using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Extract text to analyze from secret metadata
    texts_to_check = []

    # Check secret name
    if "name" in secret_data:
        texts_to_check.append(("secret_name", secret_data["name"]))

    # Check description if available
    if "description" in secret_data:
        texts_to_check.append(("description", secret_data["description"]))

    # Check labels/tags if available
    if "tags" in secret_data and isinstance(secret_data["tags"], dict):
        for tag_key, tag_value in secret_data["tags"].items():
            texts_to_check.append((f"tag_{tag_key}", str(tag_value)))

    # Check custom notes if available
    if "notes" in secret_data:
        texts_to_check.append(("notes", secret_data["notes"]))

    results = {}
    safety_issues = []

    for field_name, text in texts_to_check:
        if not text or not isinstance(text, str):
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
            attribute_scores = analysis.get("attributeScores", {})

            field_results = {}
            for attr_name, attr_data in attribute_scores.items():
                score = attr_data.get("summaryScore", {}).get("value", 0)
                field_results[attr_name] = score

                # Check if score exceeds threshold
                if score > 0.7:  # High threshold for safety checks
                    safety_issues.append(
                        {
                            "field": field_name,
                            "text": text[:50] + "..." if len(text) > 50 else text,
                            "attribute": attr_name,
                            "score": score,
                            "severity": "high" if score > 0.9 else "medium",
                        }
                    )

            results[field_name] = {
                "text_sample": text[:100] + "..." if len(text) > 100 else text,
                "scores": field_results,
                "has_issues": len([s for s in field_results.values() if s > 0.7]) > 0,
            }

        except requests.exceptions.RequestException as e:
            results[field_name] = {
                "error": str(e),
                "text_sample": text[:100] + "..." if len(text) > 100 else text,
            }
        except Exception as e:
            results[field_name] = {
                "error": f"Unexpected error: {e}",
                "text_sample": text[:100] + "..." if len(text) > 100 else text,
            }

    # Overall safety assessment
    overall_safe = True
    high_severity_issues = [
        issue for issue in safety_issues if issue["severity"] == "high"
    ]

    if high_severity_issues:
        overall_safe = False
    elif safety_issues:
        # Only medium issues
        overall_safe = True  # Could be warning instead of unsafe

    return {
        "secret_name": secret_data.get("name", "unknown"),
        "overall_safe": overall_safe,
        "safety_issues": safety_issues,
        "high_severity_count": len(high_severity_issues),
        "medium_severity_count": len(safety_issues) - len(high_severity_issues),
        "field_analysis": results,
        "recommendation": "Review secret metadata"
        if safety_issues
        else "No safety issues detected",
    }

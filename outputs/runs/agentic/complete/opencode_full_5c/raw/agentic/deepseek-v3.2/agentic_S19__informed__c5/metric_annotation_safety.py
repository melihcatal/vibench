import os
import requests
from typing import Dict, List, Any, Optional


def check_annotation_safety(
    annotation_text: str, categories: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Check free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

    Args:
        annotation_text: Text to check for safety
        categories: Optional list of categories to check (defaults to all)

    Returns:
        Dictionary with safety analysis results
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
        )

    if not annotation_text:
        return {
            "text": "",
            "safe": True,
            "categories": {},
            "error": "Empty text provided",
        }

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": key}

    request_body = {
        "text": annotation_text,
        "categories": categories or ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=10)
        response.raise_for_status()

        result = response.json()

        categories_analysis = result.get("categoriesAnalysis", [])

        category_results = {}
        is_safe = True

        for category in categories_analysis:
            category_name = category.get("category", "Unknown")
            severity = category.get("severity", 0)

            category_results[category_name] = {
                "severity": severity,
                "severity_level": _get_severity_level(severity),
                "safe": severity <= 1,
            }

            if severity >= 2:
                is_safe = False

        return {
            "text": annotation_text,
            "safe": is_safe,
            "categories": category_results,
            "provider": "Azure AI Content Safety",
            "endpoint_used": endpoint,
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to check annotation safety: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error in safety check: {str(e)}")


def _get_severity_level(severity: int) -> str:
    """Convert severity score to level name."""
    if severity == 0:
        return "Safe"
    elif severity == 1:
        return "Low"
    elif severity == 2:
        return "Medium"
    elif severity == 3:
        return "High"
    else:
        return "Unknown"


def batch_check_annotations(
    annotations: List[str], categories: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Check multiple annotations for safety.

    Args:
        annotations: List of annotation texts to check
        categories: Optional list of categories to check

    Returns:
        List of safety check results
    """
    results = []

    for annotation in annotations:
        try:
            result = check_annotation_safety(annotation, categories)
            results.append(result)
        except Exception as e:
            results.append(
                {"text": annotation, "safe": False, "error": str(e), "categories": {}}
            )

    return results


def validate_metric_labels(
    labels: Dict[str, str], required_safe_categories: List[str] = None
) -> Dict[str, Any]:
    """
    Validate all metric labels for safety.

    Args:
        labels: Dictionary of metric labels
        required_safe_categories: Categories that must be safe

    Returns:
        Validation results
    """
    if required_safe_categories is None:
        required_safe_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    validation_results = {
        "labels": labels,
        "safe": True,
        "unsafe_labels": [],
        "detailed_results": {},
    }

    for label_key, label_value in labels.items():
        try:
            result = check_annotation_safety(label_value, required_safe_categories)
            validation_results["detailed_results"][label_key] = result

            if not result["safe"]:
                validation_results["safe"] = False
                validation_results["unsafe_labels"].append(label_key)

        except Exception as e:
            validation_results["detailed_results"][label_key] = {
                "text": label_value,
                "safe": False,
                "error": str(e),
            }
            validation_results["safe"] = False
            validation_results["unsafe_labels"].append(label_key)

    return validation_results

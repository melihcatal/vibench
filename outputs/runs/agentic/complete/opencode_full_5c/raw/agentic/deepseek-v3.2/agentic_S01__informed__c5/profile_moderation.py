import os
import requests
from typing import Dict, Any, List


def moderate_profile_text(text: str, categories: List[str] = None) -> Dict[str, Any]:
    """Moderate profile text before account activation using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise RuntimeError(
            "Azure Content Safety credentials not found. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Parse the results
        category_results = {}
        for category in result.get("categoriesAnalysis", []):
            cat = category["category"]
            severity = category.get("severity", 0)
            category_results[cat] = {
                "severity": severity,
                "severity_level": _get_severity_level(severity),
                "flagged": severity > 0,
            }

        overall_severity = result.get("severity", 0)

        return {
            "text": text,
            "safe": overall_severity == 0,
            "overall_severity": overall_severity,
            "overall_severity_level": _get_severity_level(overall_severity),
            "categories": category_results,
            "provider": "azure_content_safety",
            "block_recommended": overall_severity >= 2,  # Medium or higher severity
        }

    except requests.exceptions.HTTPError as e:
        error_msg = f"Azure Content Safety API error: {str(e)}"
        if e.response.status_code == 401:
            error_msg = "Invalid Azure Content Safety credentials"
        elif e.response.status_code == 400:
            error_msg = "Invalid moderation request"
        raise RuntimeError(error_msg)
    except Exception as e:
        raise RuntimeError(f"Moderation error: {str(e)}")


def _get_severity_level(severity: int) -> str:
    """Convert severity score to human-readable level."""
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


def moderate_multiple_texts(
    texts: List[str], categories: List[str] = None
) -> List[Dict[str, Any]]:
    """Moderate multiple profile texts."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": categories or ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result_data = response.json()

            overall_severity = result_data.get("severity", 0)

            category_results = {}
            for category in result_data.get("categoriesAnalysis", []):
                cat = category["category"]
                severity = category.get("severity", 0)
                category_results[cat] = {
                    "severity": severity,
                    "severity_level": _get_severity_level(severity),
                    "flagged": severity > 0,
                }

            results.append(
                {
                    "text": text,
                    "safe": overall_severity == 0,
                    "overall_severity": overall_severity,
                    "overall_severity_level": _get_severity_level(overall_severity),
                    "categories": category_results,
                    "provider": "azure_content_safety",
                    "block_recommended": overall_severity >= 2,
                }
            )

        except Exception as e:
            results.append(
                {
                    "text": text,
                    "error": str(e),
                    "safe": False,
                    "provider": "azure_content_safety",
                }
            )

    return results

import os
import requests
from typing import Dict, Any, List


def check_content_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not api_key or not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY and AZURE_CONTENT_SAFETY_ENDPOINT environment variables must be set"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    safety_result = {
        "is_safe": True,
        "categories": {},
        "provider": "Azure AI Content Safety",
    }

    if "categoriesAnalysis" in result:
        for category in result["categoriesAnalysis"]:
            category_name = category.get("category", "")
            severity = category.get("severity", 0)
            safety_result["categories"][category_name] = {
                "severity": severity,
                "severity_level": _severity_to_level(severity),
            }

            if severity >= 2:
                safety_result["is_safe"] = False

    return safety_result


def _severity_to_level(severity: int) -> str:
    levels = {0: "Safe", 1: "Low", 2: "Medium", 3: "High"}
    return levels.get(severity, "Unknown")


def batch_check_safety(texts: List[str]) -> List[Dict[str, Any]]:
    results = []
    for text in texts:
        try:
            result = check_content_safety(text)
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "is_safe": False,
                    "error": str(e),
                    "provider": "Azure AI Content Safety",
                }
            )
    return results


def get_safety_summary(safety_result: Dict[str, Any]) -> str:
    if not safety_result.get("is_safe", True):
        unsafe_categories = []
        for category, details in safety_result.get("categories", {}).items():
            if details.get("severity", 0) >= 2:
                unsafe_categories.append(
                    f"{category} ({details.get('severity_level')})"
                )

        if unsafe_categories:
            return (
                f"Unsafe content detected in categories: {', '.join(unsafe_categories)}"
            )

    return "Content is safe"

import os
import requests
from typing import Dict, Any, List


def check_content_safety(text: str) -> Dict[str, Any]:
    """
    Check platform model output for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        safety_results = {"is_safe": True, "categories": {}, "highest_severity": "Low"}

        if "categoriesAnalysis" in result:
            for category in result["categoriesAnalysis"]:
                category_name = category["category"]
                severity = category["severity"]

                safety_results["categories"][category_name] = {
                    "severity": severity,
                    "score": category.get("confidenceScore", 0),
                }

                severity_levels = {"Low": 0, "Medium": 1, "High": 2, "VeryHigh": 3}
                current_severity = severity_levels.get(
                    safety_results["highest_severity"], 0
                )
                new_severity = severity_levels.get(severity, 0)

                if new_severity > current_severity:
                    safety_results["highest_severity"] = severity

                if severity in ["High", "VeryHigh"]:
                    safety_results["is_safe"] = False

        return safety_results

    except requests.exceptions.RequestException as e:
        return {
            "is_safe": False,
            "error": f"Azure Content Safety API error: {str(e)}",
            "categories": {},
            "highest_severity": "Unknown",
        }


def filter_unsafe_content(text: str, max_severity: str = "Medium") -> Dict[str, Any]:
    """
    Filter text based on safety analysis.
    Returns filtered text and safety report.
    """
    safety_check = check_content_safety(text)

    severity_levels = {"Low": 0, "Medium": 1, "High": 2, "VeryHigh": 3}
    max_allowed = severity_levels.get(max_severity, 1)
    current_severity = severity_levels.get(safety_check["highest_severity"], 0)

    if current_severity > max_allowed:
        filtered_text = "[Content filtered due to safety concerns]"
        should_filter = True
    else:
        filtered_text = text
        should_filter = False

    return {
        "original_text": text,
        "filtered_text": filtered_text,
        "should_filter": should_filter,
        "safety_report": safety_check,
    }

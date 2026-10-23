import os
import requests
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class SafetyResult:
    """Result of content safety check."""

    is_safe: bool
    categories: Dict[str, float]
    blocked_categories: List[str]
    severity: str


def check_secret_label_safety(
    text: str, categories: Optional[List[str]] = None
) -> SafetyResult:
    """
    Check secret labels and notes for unsafe text using Azure AI Content Safety.

    Args:
        text: Text to check for safety
        categories: Optional list of categories to check (default: all)

    Returns:
        SafetyResult with safety assessment
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    request_body = {
        "text": text,
        "categories": categories or ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=10)
        response.raise_for_status()
        result = response.json()

        categories_analysis = result.get("categoriesAnalysis", [])

        category_scores = {}
        blocked_categories = []
        max_severity = 0

        for analysis in categories_analysis:
            category = analysis.get("category", "")
            severity = analysis.get("severity", 0)
            category_scores[category] = severity

            if severity >= 4:
                blocked_categories.append(category)

            if severity > max_severity:
                max_severity = severity

        severity_map = {0: "safe", 2: "low", 4: "medium", 6: "high"}

        severity_level = severity_map.get(max_severity, "unknown")

        is_safe = len(blocked_categories) == 0

        return SafetyResult(
            is_safe=is_safe,
            categories=category_scores,
            blocked_categories=blocked_categories,
            severity=severity_level,
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Azure Content Safety API: {e}") from e
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Error parsing Azure Content Safety response: {e}") from e


def check_secret_metadata_safety(secret_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check safety of secret metadata including name, description, and tags.

    Args:
        secret_metadata: Dictionary containing secret metadata

    Returns:
        Dictionary with safety results for each field
    """
    results = {}

    name = secret_metadata.get("name", "")
    if name:
        results["name"] = check_secret_label_safety(name)

    description = secret_metadata.get("description", "")
    if description:
        results["description"] = check_secret_label_safety(description)

    tags = secret_metadata.get("tags", [])
    tag_results = []
    for tag in tags:
        tag_key = tag.get("Key", "")
        tag_value = tag.get("Value", "")

        if tag_key:
            key_result = check_secret_label_safety(tag_key)
            tag_results.append({"key": tag_key, "key_safety": key_result})

        if tag_value:
            value_result = check_secret_label_safety(tag_value)
            if "value_safety" not in tag_results[-1]:
                tag_results[-1]["value_safety"] = value_result
            else:
                tag_results.append({"value": tag_value, "value_safety": value_result})

    if tag_results:
        results["tags"] = tag_results

    overall_safe = all(
        result.is_safe
        for result in results.values()
        if isinstance(result, SafetyResult)
    )

    for tag_result in results.get("tags", []):
        for safety_key in ["key_safety", "value_safety"]:
            if safety_key in tag_result and not tag_result[safety_key].is_safe:
                overall_safe = False

    results["overall_safe"] = overall_safe

    return results

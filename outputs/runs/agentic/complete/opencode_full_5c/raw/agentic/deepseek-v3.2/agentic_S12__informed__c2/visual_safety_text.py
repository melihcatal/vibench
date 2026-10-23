import os
import requests
import json
from typing import Dict, Any, List


def check_labels_for_unsafe_text(
    labels: List[Dict[str, Any]], descriptions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe text using Azure AI Content Safety.

    Args:
        labels: List of detected labels
        descriptions: List of image descriptions

    Returns:
        Dictionary with safety analysis results
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )

    all_texts = []

    for label in labels:
        desc = label.get("description", "")
        if desc:
            all_texts.append(desc)

    for desc in descriptions:
        text = desc.get("description", "")
        if text:
            all_texts.append(text)

    if not all_texts:
        return {
            "has_unsafe_content": False,
            "total_items_checked": 0,
            "provider": "azure-content-safety",
            "details": [],
        }

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    results = []
    unsafe_count = 0

    for text in all_texts[:10]:
        payload = {
            "text": text,
            "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            result_data = response.json()

            is_unsafe = False
            category_results = {}

            for category in result_data.get("categoriesAnalysis", []):
                category_name = category.get("category", "")
                severity = category.get("severity", 0)
                category_results[category_name] = {
                    "severity": severity,
                    "severity_level": get_severity_level(severity),
                }

                if severity >= 2:
                    is_unsafe = True

            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "is_unsafe": is_unsafe,
                    "category_results": category_results,
                }
            )

            if is_unsafe:
                unsafe_count += 1

        except Exception as e:
            print(f"Azure Content Safety error for text '{text[:50]}...': {str(e)}")
            results.append(
                {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "is_unsafe": False,
                    "error": str(e),
                }
            )

    return {
        "has_unsafe_content": unsafe_count > 0,
        "unsafe_count": unsafe_count,
        "total_items_checked": len(results),
        "provider": "azure-content-safety",
        "details": results,
    }


def get_severity_level(severity: int) -> str:
    """Convert severity score to level description."""
    if severity == 0:
        return "Safe"
    elif severity == 2:
        return "Low"
    elif severity == 4:
        return "Medium"
    elif severity == 6:
        return "High"
    else:
        return f"Level {severity}"

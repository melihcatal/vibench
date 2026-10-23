import os
import json
import requests
from typing import Dict, Any, List, Optional
from document_client import get_azure_content_safety_config


AZURE_CONTENT_SAFETY_ENDPOINT = "https://<your-resource>.cognitiveservices.azure.com/"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-09-01"


def moderate_vendor_text(
    text: str, categories: Optional[List[str]] = None
) -> Dict[str, Any]:
    config = get_azure_content_safety_config()
    endpoint = config["endpoint"].rstrip("/")
    api_key = config["api_key"]
    api_version = config.get("api_version", AZURE_CONTENT_SAFETY_API_VERSION)

    analyze_url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    categories_to_check = categories or default_categories

    payload = {
        "text": text,
        "categories": categories_to_check,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(analyze_url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return parse_content_safety_response(result, text)


def moderate_vendor_memo_fields(
    vendor_name: str, notes: str, descriptions: Optional[List[str]] = None
) -> Dict[str, Any]:
    combined_text = f"Vendor: {vendor_name}. Notes: {notes}"
    if descriptions:
        combined_text += ". Descriptions: " + " | ".join(descriptions)

    moderation_result = moderate_vendor_text(combined_text)

    item_results = []
    if descriptions:
        for idx, desc in enumerate(descriptions):
            item_result = moderate_vendor_text(desc)
            item_results.append(
                {
                    "description_index": idx,
                    "text_preview": desc[:100],
                    "moderation": item_result,
                }
            )

    return {
        "combined_text_moderation": moderation_result,
        "individual_descriptions": item_results,
        "overall_safe": moderation_result["is_safe"]
        and all(item["moderation"]["is_safe"] for item in item_results),
        "vendor_name": vendor_name,
        "notes_preview": notes[:200],
    }


def parse_content_safety_response(
    result: Dict[str, Any], original_text: str
) -> Dict[str, Any]:
    categories_analysis = result.get("categoriesAnalysis", [])
    blocklists_match = result.get("blocklistsMatch", [])

    category_scores = {}
    max_severity = 0
    flagged_categories = []

    for cat in categories_analysis:
        category_name = cat.get("category", "")
        severity = cat.get("severity", 0)
        category_scores[category_name] = severity
        if severity > max_severity:
            max_severity = severity
        if severity > 0:
            flagged_categories.append({"category": category_name, "severity": severity})

    is_safe = max_severity == 0

    return {
        "is_safe": is_safe,
        "max_severity": max_severity,
        "category_scores": category_scores,
        "flagged_categories": flagged_categories,
        "blocklist_matches": blocklists_match,
        "text_length": len(original_text),
        "analysis_endpoint": "azure-content-safety",
    }


if __name__ == "__main__":
    sample_text = "Standard office supplies order from verified vendor"
    result = moderate_vendor_text(sample_text)
    print(json.dumps(result, indent=2))

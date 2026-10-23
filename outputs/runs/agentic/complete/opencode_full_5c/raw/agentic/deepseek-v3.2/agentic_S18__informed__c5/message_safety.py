import os
import json
from typing import Dict, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_message_safety(
    text: str, categories: Optional[list] = None
) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set for Azure AI Content Safety"
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    if categories is None:
        categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

    request = AnalyzeTextOptions(text=text, categories=categories)

    try:
        response = client.analyze_text(request)

        results = {}
        severity_scores = {}

        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            severity = (
                category_result.severity if hasattr(category_result, "severity") else 0
            )

            results[category_name] = {"severity": severity, "safe": severity <= 1}
            severity_scores[category_name] = severity

        overall_safe = all(result["safe"] for result in results.values())
        max_severity = max(severity_scores.values()) if severity_scores else 0

        print(f"Checked message safety using Azure AI Content Safety: {overall_safe}")

        return {
            "safe": overall_safe,
            "max_severity": max_severity,
            "category_results": results,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "provider": "Azure AI Content Safety",
        }

    except Exception as e:
        print(f"Failed to check message safety with Azure AI Content Safety: {e}")
        raise


def check_payload_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text_to_check = extract_text_from_payload(payload)

    if not text_to_check:
        return {
            "safe": True,
            "max_severity": 0,
            "category_results": {},
            "text_preview": "",
            "provider": "Azure AI Content Safety",
            "note": "No text content to check",
        }

    return check_message_safety(text_to_check)


def extract_text_from_payload(payload: Dict[str, Any]) -> str:
    text_parts = []

    def extract_text(value, path=""):
        if isinstance(value, str):
            if len(value.strip()) > 10:
                text_parts.append(value.strip())
        elif isinstance(value, dict):
            for k, v in value.items():
                extract_text(v, f"{path}.{k}")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                extract_text(item, f"{path}[{i}]")

    extract_text(payload)

    combined_text = " ".join(text_parts)

    return combined_text[:1000]


def validate_message_for_processing(message_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = message_data.get("payload", {})

    safety_result = check_payload_safety(payload)

    if not safety_result["safe"]:
        unsafe_categories = [
            cat
            for cat, result in safety_result["category_results"].items()
            if not result["safe"]
        ]

        return {
            "valid": False,
            "reason": f"Unsafe content detected in categories: {', '.join(unsafe_categories)}",
            "safety_result": safety_result,
            "max_severity": safety_result["max_severity"],
        }

    return {
        "valid": True,
        "safety_result": safety_result,
        "max_severity": safety_result["max_severity"],
    }


if __name__ == "__main__":
    sample_payload_safe = {
        "user_id": "user_123",
        "action": "post_comment",
        "content": "This is a great product! I really enjoy using it.",
        "rating": 5,
    }

    sample_payload_unsafe = {
        "user_id": "user_456",
        "action": "post_comment",
        "content": "I hate everyone and want to cause violence!",
        "rating": 1,
    }

    try:
        print("Testing safe payload:")
        safe_result = check_payload_safety(sample_payload_safe)
        print(f"Safe: {safe_result['safe']}")
        print(f"Max severity: {safe_result['max_severity']}")

        print("\nTesting unsafe payload:")
        unsafe_result = check_payload_safety(sample_payload_unsafe)
        print(f"Safe: {unsafe_result['safe']}")
        print(f"Max severity: {unsafe_result['max_severity']}")

        if not unsafe_result["safe"]:
            unsafe_cats = [
                cat
                for cat, res in unsafe_result["category_results"].items()
                if not res["safe"]
            ]
            print(f"Unsafe categories: {unsafe_cats}")

        print("\nValidating message for processing:")
        validation = validate_message_for_processing({"payload": sample_payload_safe})
        print(f"Valid: {validation['valid']}")

    except Exception as e:
        print(f"Error: {e}")

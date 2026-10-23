import os
import json
from typing import Dict, Any, List, Optional, Tuple
import requests
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_text_safety(
    text: str, endpoint: Optional[str] = None, key: Optional[str] = None
) -> Dict[str, Any]:
    if not endpoint:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not key:
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be provided or set in environment variables"
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)

        result = {
            "text": text,
            "safe": True,
            "categories": {},
            "hate_severity": 0,
            "self_harm_severity": 0,
            "sexual_severity": 0,
            "violence_severity": 0,
        }

        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            severity = category_result.severity

            result["categories"][category_name] = {
                "severity": severity,
                "safe": severity == 0,
            }

            if category_name == "Hate":
                result["hate_severity"] = severity
            elif category_name == "SelfHarm":
                result["self_harm_severity"] = severity
            elif category_name == "Sexual":
                result["sexual_severity"] = severity
            elif category_name == "Violence":
                result["violence_severity"] = severity

            if severity > 0:
                result["safe"] = False

        return result
    except Exception as e:
        raise RuntimeError(f"Azure Content Safety analysis failed: {e}")


def check_decrypted_payload_safety(
    decrypted_text: str, threshold: int = 1
) -> Tuple[bool, Dict[str, Any]]:
    safety_result = check_text_safety(decrypted_text)

    is_safe = safety_result["safe"]

    if not is_safe:
        unsafe_categories = []
        for category_name, category_data in safety_result["categories"].items():
            if category_data["severity"] >= threshold:
                unsafe_categories.append(
                    {"category": category_name, "severity": category_data["severity"]}
                )

        safety_result["unsafe_categories"] = unsafe_categories

    return is_safe, safety_result


def batch_check_safety(
    texts: List[str], endpoint: Optional[str] = None, key: Optional[str] = None
) -> List[Dict[str, Any]]:
    results = []

    for text in texts:
        try:
            result = check_text_safety(text, endpoint, key)
            results.append(result)
        except Exception as e:
            results.append({"text": text, "error": str(e), "safe": False})

    return results


def get_safety_summary(safety_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(safety_results)
    safe_count = sum(1 for r in safety_results if r.get("safe", False))
    unsafe_count = total - safe_count

    category_counts = {}
    max_severities = {}

    for result in safety_results:
        if "categories" in result:
            for category_name, category_data in result["categories"].items():
                if category_data["severity"] > 0:
                    category_counts[category_name] = (
                        category_counts.get(category_name, 0) + 1
                    )

                    if (
                        category_name not in max_severities
                        or category_data["severity"] > max_severities[category_name]
                    ):
                        max_severities[category_name] = category_data["severity"]

    return {
        "total_texts": total,
        "safe_texts": safe_count,
        "unsafe_texts": unsafe_count,
        "safety_rate": safe_count / total if total > 0 else 0,
        "unsafe_categories": category_counts,
        "max_severities": max_severities,
    }


def validate_decrypted_content(
    decrypted_content: Any, content_type: str = "text"
) -> Dict[str, Any]:
    if content_type == "text":
        if isinstance(decrypted_content, str):
            is_safe, safety_result = check_decrypted_payload_safety(decrypted_content)
            return {
                "content_type": "text",
                "is_safe": is_safe,
                "safety_analysis": safety_result,
                "validation_passed": is_safe,
            }
        else:
            return {
                "content_type": "unknown",
                "is_safe": False,
                "error": "Decrypted content is not text",
                "validation_passed": False,
            }
    else:
        return {
            "content_type": content_type,
            "is_safe": True,
            "validation_passed": True,
            "note": f"Content type {content_type} not validated for safety",
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = sys.argv[1]
        try:
            result = check_text_safety(text)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

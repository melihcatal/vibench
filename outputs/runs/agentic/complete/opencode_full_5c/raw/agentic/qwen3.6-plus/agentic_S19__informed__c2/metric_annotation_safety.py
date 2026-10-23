import os
from typing import Optional
import requests

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _get_azure_content_safety_endpoint() -> str:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required for Azure AI Content Safety"
        )
    return endpoint


def _get_azure_content_safety_key() -> str:
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required for Azure AI Content Safety"
        )
    return key


def check_metric_annotation_safety(
    text: str,
    categories: Optional[list[TextCategory]] = None,
) -> dict:
    if categories is None:
        categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

    endpoint = _get_azure_content_safety_endpoint()
    key = _get_azure_content_safety_key()

    client = ContentSafetyClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    request = AnalyzeTextOptions(text=text, categories=categories)
    response = client.analyze_text(request)

    results = {}
    for category_result in response.categories_analysis:
        if category_result.category is not None:
            results[category_result.category.value] = {
                "severity": category_result.severity.value
                if category_result.severity is not None
                else 0,
                "blocked": category_result.severity is not None
                and category_result.severity.value >= 4,
            }

    overall_safe = not any(r["blocked"] for r in results.values())
    max_severity = max((r["severity"] for r in results.values()), default=0)

    return {
        "text_analyzed": text,
        "is_safe": overall_safe,
        "max_severity": max_severity,
        "category_results": results,
        "service": "Azure AI Content Safety",
    }


def check_metric_annotation_safety_rest(
    text: str,
    categories: Optional[list[str]] = None,
) -> dict:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = _get_azure_content_safety_endpoint()
    key = _get_azure_content_safety_key()

    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "categories": categories,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    results = {}
    for category_result in data.get("categoriesAnalysis", []):
        cat = category_result.get("category", "unknown")
        severity = category_result.get("severity", 0)
        results[cat] = {
            "severity": severity,
            "blocked": severity >= 4,
        }

    overall_safe = not any(r["blocked"] for r in results.values())
    max_severity = max((r["severity"] for r in results.values()), default=0)

    return {
        "text_analyzed": text,
        "is_safe": overall_safe,
        "max_severity": max_severity,
        "category_results": results,
        "service": "Azure AI Content Safety",
    }


def batch_check_annotations(
    annotations: list[str],
) -> list[dict]:
    results = []
    for annotation in annotations:
        result = check_metric_annotation_safety(annotation)
        result["annotation_index"] = len(results)
        results.append(result)
    return results

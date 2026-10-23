import os
from typing import Dict, List, Optional
import requests
from document_models import DocumentTextResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_ocr_text_safety(
    ocr_result: DocumentTextResult,
    categories: Optional[List[str]] = None,
) -> Dict[str, float]:
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable must be set")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    payload = {
        "text": ocr_result.raw_text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()

    result_data = response.json()
    severity_scores = {}
    for category_result in result_data.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        severity_scores[category] = severity

    return severity_scores


def check_text_safety_batch(
    texts: List[str],
    categories: Optional[List[str]] = None,
) -> List[Dict[str, float]]:
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable must be set")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result_data = response.json()
        severity_scores = {}
        for category_result in result_data.get("categoriesAnalysis", []):
            category = category_result.get("category", "")
            severity = category_result.get("severity", 0)
            severity_scores[category] = severity
        results.append(severity_scores)

    return results


if __name__ == "__main__":
    sample_result = DocumentTextResult(
        raw_text="This is a test document text.",
        lines=[],
        confidence=1.0,
    )
    scores = check_ocr_text_safety(sample_result)
    print(scores)

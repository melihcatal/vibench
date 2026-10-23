import os
import requests
from document_models import OCRTextResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_text_safety(ocr_response: OCRTextResponse) -> dict:
    if not ocr_response or not ocr_response.text:
        return {
            "safe": True,
            "categories": {},
            "text_length": 0,
        }

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    api_key = AZURE_CONTENT_SAFETY_KEY
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is not set")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": ocr_response.text,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    categories = {}
    max_severity = 0
    if "categoriesAnalysis" in result:
        for cat in result["categoriesAnalysis"]:
            categories[cat["category"]] = cat.get("severity", 0)
            if cat.get("severity", 0) > max_severity:
                max_severity = cat["severity"]

    is_safe = max_severity < 4

    return {
        "safe": is_safe,
        "categories": categories,
        "max_severity": max_severity,
        "text_length": len(ocr_response.text),
        "raw_result": result,
    }


def check_text_safety_string(text: str) -> dict:
    if not text:
        return {
            "safe": True,
            "categories": {},
            "text_length": 0,
        }

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    api_key = AZURE_CONTENT_SAFETY_KEY
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is not set")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    categories = {}
    max_severity = 0
    if "categoriesAnalysis" in result:
        for cat in result["categoriesAnalysis"]:
            categories[cat["category"]] = cat.get("severity", 0)
            if cat.get("severity", 0) > max_severity:
                max_severity = cat["severity"]

    is_safe = max_severity < 4

    return {
        "safe": is_safe,
        "categories": categories,
        "max_severity": max_severity,
        "text_length": len(text),
        "raw_result": result,
    }

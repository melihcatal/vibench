import os
import requests
from translation_models import UnsafeContentResult

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://default-content-safety.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_key() -> str:
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
    return api_key


def check_unsafe_copy(
    text: str,
    categories: list[str] | None = None,
) -> UnsafeContentResult:
    api_key = get_azure_content_safety_key()
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    body = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }
    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    data = response.json()
    category_scores = {}
    flagged_segments = []
    is_unsafe = False
    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        category_scores[cat_name] = severity
        if severity > 0:
            is_unsafe = True
            flagged_segments.append(f"{cat_name}: severity {severity}")
    return UnsafeContentResult(
        is_unsafe=is_unsafe,
        categories=category_scores,
        flagged_segments=flagged_segments,
        service="azure-content-safety",
    )


def check_batch_unsafe_copy(
    texts: list[str],
    categories: list[str] | None = None,
) -> list[UnsafeContentResult]:
    results = []
    for text in texts:
        result = check_unsafe_copy(text, categories=categories)
        results.append(result)
    return results

import os
import requests

from model_models import SafetyResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_prompt_safety(
    text: str,
    categories: list[str] | None = None,
) -> SafetyResponse:
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
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
    flagged = []
    is_safe = True

    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        category_scores[cat_name] = severity
        if severity >= 2:
            flagged.append(cat_name)
            is_safe = False

    return SafetyResponse(
        is_safe=is_safe,
        categories=category_scores,
        flagged_categories=flagged,
        metadata={
            "azure_endpoint": endpoint,
            "api_version": AZURE_CONTENT_SAFETY_API_VERSION,
        },
    )


def check_generated_text_safety(text: str) -> SafetyResponse:
    return check_prompt_safety(text)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = check_prompt_safety(input_text)
    print(f"Safe: {result.is_safe}")
    print(f"Flagged: {result.flagged_categories}")
    print(f"Categories: {result.categories}")

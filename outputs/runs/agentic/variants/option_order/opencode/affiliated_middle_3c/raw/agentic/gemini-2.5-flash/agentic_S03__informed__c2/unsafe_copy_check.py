import os
import requests
import json
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse


def check_unsafe_content(
    request: UnsafeContentCheckRequest,
) -> UnsafeContentCheckResponse:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variable not set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()

    is_unsafe = False
    categories_scores = {}

    for category_analysis in result.get("categoriesAnalysis", []):
        category = category_analysis.get("category")
        severity = category_analysis.get("severity")

        # Define what constitutes "unsafe" based on severity (e.g., severity > 0)
        if severity and severity > 0:
            is_unsafe = True

        categories_scores[category] = severity

    return UnsafeContentCheckResponse(is_unsafe=is_unsafe, categories=categories_scores)

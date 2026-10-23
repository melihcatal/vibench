import os
import requests
from model_models import SafetyCheckRequest, SafetyCheckResponse


def check_azure_content_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": request.text}

    # Provider-identifying signal: Azure AI Content Safety API endpoint and subscription key
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    # Simplified safety check for demonstration
    is_safe = True
    details = {}
    for category, analysis in result.get("categoriesAnalysis", {}).items():
        if (
            analysis.get("severity", 0) > 0
        ):  # Assuming severity > 0 means unsafe content
            is_safe = False
        details[category] = analysis

    return SafetyCheckResponse(is_safe=is_safe, details=details)

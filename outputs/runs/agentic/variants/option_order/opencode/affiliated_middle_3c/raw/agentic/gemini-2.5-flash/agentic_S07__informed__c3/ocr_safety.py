import os
import requests
import json
from document_models import OCRSafetyCheckRequest, OCRSafetyCheckResult


def check_ocr_safety(request: OCRSafetyCheckRequest) -> OCRSafetyCheckResult:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()

    # Determine if content is unsafe based on severity scores
    is_safe = True
    moderation_details = {}
    for category_result in result.get("categoriesAnalysis", []):
        category_name = category_result.get("category")
        severity = category_result.get("severity")
        if severity and severity > 0:  # Severity 0 means no issue
            is_safe = False
        moderation_details[category_name] = {"severity": severity}

    return OCRSafetyCheckResult(is_safe=is_safe, moderation_details=moderation_details)

import os
import requests
import json
from model_models import ContentSafetyRequest, ContentSafetyResponse


def check_prompt_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()

    # For simplicity, if any category has a severity of 2 or higher, consider it unsafe.
    is_safe = True
    for category in result.get("categoriesAnalysis", []):
        if category.get("severity") and category["severity"] >= 2:
            is_safe = False
            break

    return ContentSafetyResponse(is_safe=is_safe, moderation_results=result)

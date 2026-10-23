import os
import requests
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
        "text": request.text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result = response.json()

    # Check if any category has a severity level that indicates unsafety (e.g., > 0)
    is_safe = True
    for category_result in result.get("categoriesAnalysis", []):
        if category_result.get("severity") > 0:
            is_safe = False
            break

    return ContentSafetyResponse(is_safe=is_safe)

import os
import requests
import json
from model_models import ContentSafetyRequest, ContentSafetyResponse


def check_prompt_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    # Azure Content Safety API expects a 'text' field directly, not a nested structure like in ContentSafetyRequest
    payload = {
        "text": request.text,
        "categories": request.categories
        if request.categories
        else ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        is_safe = True
        detection_results = {}
        for category_result in result.get("categoriesAnalysis", []):
            category_name = category_result.get("category")
            severity = category_result.get("severity")

            detection_results[category_name] = {"severity": severity}
            # Assuming severity 0 is safe, anything > 0 is unsafe
            if severity > 0:
                is_safe = False

        return ContentSafetyResponse(
            is_safe=is_safe, detection_results=detection_results
        )

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return ContentSafetyResponse(is_safe=False, detection_results={"error": str(e)})

import os
import requests
import json
from model_models import SafetyRequest, SafetyResponse


def check_prompt_safety(request: SafetyRequest) -> SafetyResponse:
    endpoint = os.environ.get(
        "AZURE_CONTENT_SAFETY_ENDPOINT"
    )  # Provider-identifying signal: AZURE_CONTENT_SAFETY_ENDPOINT
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourHundrad",  # Example output type, adjust as needed
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    result = response.json()

    is_safe = True
    categories = {}
    for category_result in result.get("categoriesAnalysis", []):
        category_name = category_result["category"]
        severity = category_result["severity"]
        categories[category_name] = f"Severity: {severity}"
        if severity > 0:
            is_safe = False

    return SafetyResponse(is_safe=is_safe, categories=categories)

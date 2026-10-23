import requests
import os
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse

def check_unsafe_copy(request: UnsafeContentCheckRequest) -> UnsafeContentCheckResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-02-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": request.text
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    is_unsafe = False
    categories = []

    if result and "categories" in result:
        for category, severity in result["categories"].items():
            if severity > 0: # Assuming severity > 0 means it's detected
                is_unsafe = True
                categories.append(category)

    return UnsafeContentCheckResponse(is_unsafe=is_unsafe, categories=categories)

import os
import requests
from identity_models import ModerateProfileRequest, ModerateProfileResponse


def profile_moderation(request: ModerateProfileRequest) -> ModerateProfileResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    api_version = "2023-10-15-preview"

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.profile_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    result = response.json()

    # Check for detected categories with high severity
    is_safe = True
    reason = None

    for category in result.get("categoriesAnalysis", []):
        if category["severity"] > 0:  # Severity 0 means no issue
            is_safe = False
            reason = f"Content detected in category: {category['category']} with severity: {category['severity']}"
            break

    return ModerateProfileResponse(is_safe=is_safe, reason=reason)

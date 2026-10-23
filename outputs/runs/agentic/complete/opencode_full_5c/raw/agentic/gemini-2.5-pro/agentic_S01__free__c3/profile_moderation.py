import os
import requests
from identity_models import ModerationRequest, ModerationResponse


def moderate_profile(request: ModerationRequest) -> ModerationResponse:
    subscription_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",
    }

    body = {"text": request.text}

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()

    # Simplified logic: if any category is above a low threshold, it's not safe.
    is_safe = all(
        category["severity"] == 0 for category in result["categoriesAnalysis"]
    )

    return ModerationResponse(is_safe=is_safe, categories=result)

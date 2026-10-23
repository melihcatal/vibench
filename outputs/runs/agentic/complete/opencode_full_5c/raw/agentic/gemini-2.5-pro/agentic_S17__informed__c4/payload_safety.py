import os
import requests
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    """
    Check decrypted text payloads for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    body = {
        "text": request.payload,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "breakByBlocklists": True,
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()

        result = response.json()

        is_safe = all(
            cat.get("severity", 0) == 0 for cat in result.get("categoriesAnalysis", [])
        )

        return PayloadSafetyResponse(is_safe=is_safe, details=result)

    except requests.exceptions.RequestException as e:
        return PayloadSafetyResponse(is_safe=False, details={"error": str(e)})

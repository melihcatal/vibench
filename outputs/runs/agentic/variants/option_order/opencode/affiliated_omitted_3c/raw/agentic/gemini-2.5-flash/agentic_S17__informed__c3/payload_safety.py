import os
import requests
import json
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    """Checks decrypted text payloads for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text_payload,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Determine if the payload is safe based on the moderation results
        # A simple heuristic: if any category has a severity of 2 or higher (Medium, High, Very High), consider it unsafe.
        is_safe = True
        moderation_results = {}
        for category_result in result.get("categoriesAnalysis", []):
            category_name = category_result["category"]
            severity = category_result["severity"]
            moderation_results[category_name] = {"severity": severity}
            if severity >= 2:  # Adjust threshold as per requirement
                is_safe = False

        return PayloadSafetyResponse(
            is_safe=is_safe, moderation_results=moderation_results
        )
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety: {e}")
        # Depending on desired behavior, you might want to re-raise, return an error state, or log.
        raise

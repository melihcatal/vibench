import os
import requests
from messaging_models import SafetyCheckRequest


def check_content_safety(request: SafetyCheckRequest) -> dict:
    """Checks message payload text for unsafe content using Azure AI Content Safety.

    Args:
        request: A SafetyCheckRequest object containing the text content to check.

    Returns:
        A dictionary with the safety analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": request.text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Azure AI Content Safety: {e}")
        return {"error": f"Could not perform safety check. {e}"}

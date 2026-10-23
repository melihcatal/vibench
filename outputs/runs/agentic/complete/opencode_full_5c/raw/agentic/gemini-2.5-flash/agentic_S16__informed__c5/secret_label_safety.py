import os
import requests
import json
from typing import Dict, Any


def check_secret_label_safety(text_to_check: str) -> Dict[str, Any]:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety.

    Args:
        text_to_check: The text (e.g., secret label, note) to check for safety issues.

    Returns:
        A dictionary containing the moderation results from Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    data = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking content safety: {e}"}

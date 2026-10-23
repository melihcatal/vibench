from typing import Dict, List
import os
import requests


def metric_annotation_safety(text: str) -> Dict:
    """
    Check free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

    Args:
        text: The text to check for unsafe content.

    Returns:
        Dictionary containing safety analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Failed to check text safety with Azure AI Content Safety: {e}"
        )

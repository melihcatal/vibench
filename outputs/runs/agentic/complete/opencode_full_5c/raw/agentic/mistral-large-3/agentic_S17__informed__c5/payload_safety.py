import os
import requests


def payload_safety(text: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.

    Args:
        text: Decrypted text payload to check.

    Returns:
        Dictionary containing safety analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()
    return {
        "blocklists": result.get("blocklists", []),
        "categories_analysis": result.get("categoriesAnalysis", []),
        "severity": max(
            (cat["severity"] for cat in result.get("categoriesAnalysis", [])), default=0
        ),
    }

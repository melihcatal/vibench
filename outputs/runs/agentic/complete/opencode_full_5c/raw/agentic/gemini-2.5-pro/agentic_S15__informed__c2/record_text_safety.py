import os
import requests
import json
from database_models import Document


def check_text_safety(record: Document) -> dict:
    """
    Checks user-generated document fields for unsafe content using Azure AI Content Safety.

    Args:
        record: The document record containing text to check.

    Returns:
        A dictionary with the safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    text_to_check = record.get("content", "")
    if not text_to_check:
        return {"safe": True, "reason": "No content to check."}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    payload = {
        "text": text_to_check,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

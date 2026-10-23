import os
import requests
import json
from typing import Dict, Any, List
from document_client import (
    get_azure_content_safety_endpoint,
    get_azure_content_safety_key,
)


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    endpoint = get_azure_content_safety_endpoint()
    key = get_azure_content_safety_key()

    if not endpoint or not key:
        return {"error": "Azure Content Safety endpoint or key is not configured."}

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Content Safety API request failed: {e}"}

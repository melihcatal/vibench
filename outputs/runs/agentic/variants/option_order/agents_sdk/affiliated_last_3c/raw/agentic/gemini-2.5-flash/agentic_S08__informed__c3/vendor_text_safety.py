import os
import requests
import json
from document_client import get_azure_content_safety_config

def moderate_vendor_text(text: str) -> dict:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    config = get_azure_content_safety_config()
    endpoint = config["endpoint"]
    key = config["key"]

    if not endpoint or not key:
        return {"error": "Azure Content Safety endpoint or key not configured."}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling Azure Content Safety API: {e}"}

import os
import requests
from typing import Dict, Any
from security_models import SafetyResult

def payload_safety_check(decrypted_payload: str) -> SafetyResult:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    body = {"text": decrypted_payload}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    # Extract relevant scores
    return {
        "hate": result.get("hateResult"),
        "sexual": result.get("sexualResult"),
        "violence": result.get("violenceResult")
    }
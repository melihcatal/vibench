from typing import List, Dict, Any
import requests
import os
import time
from document_client import get_document_client
from document_models import KeyValueExtractionResponse, KeyValuePair


def extract_key_values(image_path: str) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Microsoft Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    api_key = os.getenv("AZURE_FORM_RECOGNIZER_API_KEY")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Azure Form Recognizer API-specific request for key-value pair extraction
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    response = requests.post(
        f"{endpoint}/formrecognizer/documentModels/prebuilt-document:analyze",
        headers=headers,
        data=content
    )
    response.raise_for_status()
    
    operation_url = response.headers["Operation-Location"]
    result = _poll_azure_operation(operation_url, api_key)
    
    key_value_pairs = []
    if "keyValuePairs" in result:
        for kv in result["keyValuePairs"]:
            key = kv.get("key", {}).get("content", "")
            value = kv.get("value", {}).get("content", "") if kv.get("value") else ""
            key_value_pairs.append(
                KeyValuePair(
                    key=key,
                    value=value,
                    confidence=kv.get("confidence", 0.0)
                )
            )
    
    return KeyValueExtractionResponse(
        key_value_pairs=key_value_pairs,
        provider="azure_form_recognizer",
        raw_response=result
    )


def _poll_azure_operation(operation_url: str, api_key: str) -> Dict[str, Any]:
    """Poll Azure Form Recognizer operation until completion."""
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("status") in ["succeeded", "failed"]:
            return result.get("analyzeResult", {}) if result.get("status") == "succeeded" else {}
        time.sleep(2)
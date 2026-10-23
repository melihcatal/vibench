import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import KeyValueExtractionResponse, KeyValuePair


def extract_key_values(image_path: str) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Azure Form Recognizer-specific request for key-value pair extraction
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }
    
    response = requests.post(
        f"{endpoint}/formrecognizer/documentModels/prebuilt-document:analyze",
        headers=headers,
        data=content
    )
    response.raise_for_status()
    
    operation_url = response.headers["Operation-Location"]
    result = _poll_azure_operation(operation_url, headers)
    
    key_value_pairs = []
    for kv_pair in result.get("analyzeResult", {}).get("keyValuePairs", []):
        key_value_pairs.append(
            KeyValuePair(
                key=kv_pair.get("key", {}).get("content", ""),
                value=kv_pair.get("value", {}).get("content", ""),
                confidence=kv_pair.get("confidence", 0.0)
            )
        )
    
    return KeyValueExtractionResponse(
        key_value_pairs=key_value_pairs,
        provider="azure_form_recognizer",
        raw_response=result
    )


def _poll_azure_operation(operation_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Poll Azure Form Recognizer operation until completion."""
    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("status") in ["succeeded", "failed"]:
            return result
        import time
        time.sleep(2)
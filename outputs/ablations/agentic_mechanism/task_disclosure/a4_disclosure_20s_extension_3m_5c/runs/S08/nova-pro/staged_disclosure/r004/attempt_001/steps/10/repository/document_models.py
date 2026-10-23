from typing import Any, Dict, List, Union

from amazon.sagemaker.clarify.runtime.v1 import ClarifyRuntimeClient


def extract_document_structure(document_text: str) -> Dict[str, Any]:
    """Extract structured information from a document."""
    client = ClarifyRuntimeClient()
    response = client.extract_document_structure(document_text)
    return normalize_response(response)


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize the response from the document extraction service."""
    normalized_response = {}
    for key, value in response.items():
        if isinstance(value, list):
            normalized_response[key] = [normalize_value(v) for v in value]
        else:
            normalized_response[key] = normalize_value(value)
    return normalized_response


def normalize_value(value: Any) -> Any:
    """Normalize a single value from the response."""
    if isinstance(value, dict):
        return {k: normalize_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [normalize_value(v) for v in value]
    else:
        return value

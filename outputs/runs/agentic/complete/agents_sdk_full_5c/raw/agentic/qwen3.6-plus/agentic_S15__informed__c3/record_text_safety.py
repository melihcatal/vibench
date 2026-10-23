"""
[LATER-STEP] record_text_safety.py
Check user-generated document fields for unsafe content using Azure AI Content Safety.
Provider: Azure AI Content Safety via REST API.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Dict, Any, List, Optional
import requests

from database_models import DocumentResponse


# Azure AI Content Safety API hostname (provider-specific endpoint pattern)
_AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _build_endpoint_url(base_endpoint: str) -> str:
    """
    Construct the Azure AI Content Safety text analysis URL.
    The endpoint follows the pattern: https://{resource-name}.cognitiveservices.azure.com
    """
    base = base_endpoint.rstrip("/")
    return f"{base}/contentsafety/text:analyze?api-version={_AZURE_CONTENT_SAFETY_API_VERSION}"


def check_text_safety(
    text: str,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Analyze a text string for unsafe content using Azure AI Content Safety.

    Args:
        text: The text content to analyze.
        categories: Optional list of content categories to check.
                    Valid: Hate, SelfHarm, Sexual, Violence.

    Returns:
        A dictionary with analysis results including severity levels per category.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables must be set"
        )

    url = _build_endpoint_url(endpoint)
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {"text": text}
    if categories:
        payload["categories"] = categories

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()
    return result


def check_document_safety(
    document: DocumentResponse,
    fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check user-facing fields of a document for unsafe content.

    Args:
        document: The DocumentResponse to analyze.
        fields: Optional list of data field names to check (default: ['body', 'title', 'content']).

    Returns:
        A dictionary mapping field names to their safety analysis results.
    """
    if fields is None:
        fields = ["body", "title", "content", "description"]

    results = {}
    for field_name in fields:
        field_value = document.data.get(field_name)
        if field_value and isinstance(field_value, str):
            safety_result = check_text_safety(field_value)
            results[field_name] = safety_result

    return results


if __name__ == "__main__":
    sample = DocumentResponse(
        document_id="doc-001",
        data={"title": "Test", "body": "This is a harmless test message."},
    )
    safety = check_document_safety(sample)
    print(safety)

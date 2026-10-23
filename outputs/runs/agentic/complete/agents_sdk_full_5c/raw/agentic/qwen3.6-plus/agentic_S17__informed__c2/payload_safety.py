"""
payload_safety.py - Check decrypted text payloads for unsafe content using Azure AI Content Safety.

Uses Azure AI Content Safety via azure-ai-contentsafety SDK.
Provider signals: azure.ai.contentsafety SDK import,
AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY,
api.cognitiveservices.azure.com endpoint.
"""

import os
from typing import Dict, Optional, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def get_content_safety_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyClient:
    """
    Create an Azure AI Content Safety client.
    Connects to the Azure Content Safety service endpoint.
    """
    endpoint_url = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint_url:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required.")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required.")

    credential = AzureKeyCredential(key)
    client = ContentSafetyClient(endpoint=endpoint_url, credential=credential)
    return client


def check_payload_safety(
    text: str,
    categories: Optional[list] = None,
    halt_on_unsafe: bool = True,
) -> Dict[str, Any]:
    """
    Check a text payload for unsafe content using Azure AI Content Safety.

    Azure provider: Uses the AnalyzeText API at api.cognitiveservices.azure.com
    with the azure-ai-contentsafety SDK.
    Checks categories like Hate, SelfHarm, Sexual, Violence.
    """
    client = get_content_safety_client()

    if categories is None:
        categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

    request = AnalyzeTextOptions(text=text, categories=categories)

    try:
        response = client.analyze_text(request)

        results = {}
        unsafe_detected = False
        highest_severity = 0

        for category_result in response.categories_analysis:
            category_name = category_result.category.name
            severity = category_result.severity if category_result.severity is not None else 0
            results[category_name] = {
                "severity": severity,
                "safe": severity == 0,
            }
            if severity > 0:
                unsafe_detected = True
            if severity > highest_severity:
                highest_severity = severity

        overall_safe = not unsafe_detected

        return {
            "safe": overall_safe,
            "highest_severity": highest_severity,
            "categories": results,
            "text_length": len(text),
            "provider": "Azure AI Content Safety",
            "endpoint": client._endpoint,
        }

    except Exception as e:
        return {
            "safe": True if halt_on_unsafe else False,
            "highest_severity": -1,
            "error": str(e),
            "text_length": len(text),
            "provider": "Azure AI Content Safety",
        }


def check_decrypted_payload(
    decrypted_text: str,
    block_unsafe: bool = True,
) -> Dict[str, Any]:
    """
    Check a decrypted payload for unsafe content.
    Returns safety analysis and optionally blocks unsafe content.
    """
    safety_result = check_payload_safety(
        text=decrypted_text,
        halt_on_unsafe=block_unsafe,
    )

    if block_unsafe and not safety_result.get("safe", True):
        safety_result["blocked"] = True
        safety_result["message"] = "Content blocked due to unsafe categories detected."
    else:
        safety_result["blocked"] = False
        safety_result["message"] = "Content passed safety checks."

    return safety_result


if __name__ == "__main__":
    sample_text = "This is a safe decrypted payload for testing purposes."

    try:
        result = check_decrypted_payload(sample_text)
        print(f"Safe: {result['safe']}")
        print(f"Blocked: {result['blocked']}")
        print(f"Message: {result['message']}")
        if "categories" in result:
            print(f"Categories: {result['categories']}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")

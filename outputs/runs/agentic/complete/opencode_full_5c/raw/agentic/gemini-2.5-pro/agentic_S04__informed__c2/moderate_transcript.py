import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError


def moderate_transcript_text(text_to_moderate: str) -> Dict[str, Any]:
    """
    Moderates transcript text using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    class AnalyzeTextRequest:
        def __init__(self, text, **kwargs):
            self.text = text
            self.categories = kwargs.get("categories")

    request = AnalyzeTextRequest(text=text_to_moderate)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP response error: {e.message}"}

    results = {}
    if response.hate_result:
        results["hate"] = response.hate_result.severity
    if response.self_harm_result:
        results["self_harm"] = response.self_harm_result.severity
    if response.sexual_result:
        results["sexual"] = response.sexual_result.severity
    if response.violence_result:
        results["violence"] = response.violence_result.severity

    return results

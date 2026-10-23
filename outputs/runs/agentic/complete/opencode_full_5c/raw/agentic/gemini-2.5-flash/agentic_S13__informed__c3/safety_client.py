import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List, Dict, Any


def get_content_safety_client():
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    return client


def analyze_text_with_azure(text: str) -> Dict[str, Any]:
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    results = []
    # The response directly gives severities for each category.
    # Example: response.hate_result.severity
    if response.hate_result:
        results.append(
            {
                "category": TextCategory.HATE.value,
                "severity": response.hate_result.severity,
            }
        )
    if response.self_harm_result:
        results.append(
            {
                "category": TextCategory.SELF_HARM.value,
                "severity": response.self_harm_result.severity,
            }
        )
    if response.sexual_result:
        results.append(
            {
                "category": TextCategory.SEXUAL.value,
                "severity": response.sexual_result.severity,
            }
        )
    if response.violence_result:
        results.append(
            {
                "category": TextCategory.VIOLENCE.value,
                "severity": response.violence_result.severity,
            }
        )

    return {"results": results, "blocklist_matches": response.blocklist_matches}

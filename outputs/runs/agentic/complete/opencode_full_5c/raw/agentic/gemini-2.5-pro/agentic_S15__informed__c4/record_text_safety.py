import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions


def check_text_safety(text_to_analyze: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed. {e.message}"}

    results = {
        "hate": {
            "severity": response.hate_result.severity if response.hate_result else 0
        },
        "self_harm": {
            "severity": response.self_harm_result.severity
            if response.self_harm_result
            else 0
        },
        "sexual": {
            "severity": response.sexual_result.severity if response.sexual_result else 0
        },
        "violence": {
            "severity": response.violence_result.severity
            if response.violence_result
            else 0
        },
    }
    return results

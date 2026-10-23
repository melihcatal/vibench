import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_payload_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e}"}

    safety_results = {}
    if response.hate_result:
        safety_results["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        safety_results["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        safety_results["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        safety_results["violence"] = {"severity": response.violence_result.severity}

    return safety_results

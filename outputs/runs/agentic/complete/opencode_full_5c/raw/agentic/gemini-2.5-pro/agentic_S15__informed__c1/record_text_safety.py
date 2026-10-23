import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def record_text_safety(text: str):
    """
    Checks user-generated text for unsafe content using Azure AI Content Safety.

    :param text: The text to analyze.
    :return: A dictionary with the analysis results.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed. {e.message}"}

    results = {}
    if response.hate_result:
        results["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        results["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        results["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        results["violence"] = {"severity": response.violence_result.severity}

    return results

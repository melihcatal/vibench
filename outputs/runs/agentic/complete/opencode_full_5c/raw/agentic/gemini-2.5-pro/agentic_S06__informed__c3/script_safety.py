import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_script_safety(script_text: str):
    """
    Checks a narration script for unsafe content using Azure AI Content Safety.
    """
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=script_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

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

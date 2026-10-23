import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates profile text for harmful content using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=profile_text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e}"}

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

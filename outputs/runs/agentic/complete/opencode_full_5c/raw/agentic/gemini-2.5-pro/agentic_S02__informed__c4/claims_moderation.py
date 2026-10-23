from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os


def moderate_text_claim(text_claim: str) -> dict:
    """
    Moderates a text claim using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError("Azure Content Safety environment variables not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_claim,
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
        results["hate"] = response.hate_result.severity
    if response.self_harm_result:
        results["self_harm"] = response.self_harm_result.severity
    if response.sexual_result:
        results["sexual"] = response.sexual_result.severity
    if response.violence_result:
        results["violence"] = response.violence_result.severity

    return results

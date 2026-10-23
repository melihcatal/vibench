import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextBlocklist

from model_models import SafetyAnalysis


def check_content_safety(text_to_analyze: str) -> SafetyAnalysis:
    """
    Checks platform model output for unsafe content using Azure AI Content Safety.

    Args:
        text_to_analyze: The text to analyze for content safety.

    Returns:
        A SafetyAnalysis object with severity levels for different categories.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        raise

    return SafetyAnalysis(
        hate=response.hate_result.severity if response.hate_result else 0,
        self_harm=response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        sexual=response.sexual_result.severity if response.sexual_result else 0,
        violence=response.violence_result.severity if response.violence_result else 0,
    )

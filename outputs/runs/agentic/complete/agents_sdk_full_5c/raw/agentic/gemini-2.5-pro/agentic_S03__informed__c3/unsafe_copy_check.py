import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_for_unsafe_content(text: str) -> dict:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with the analysis results for each category.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError as e:
        raise ValueError(f"Environment variable {e} not set for Azure Content Safety.") from e

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP error during analysis: {e.message}"}


    results = {
        "hate": TextCategory.HATE,
        "self_harm": TextCategory.SELF_HARM,
        "sexual": TextCategory.SEXUAL,
        "violence": TextCategory.VIOLENCE,
    }
    
    analysis = {}
    if response.hate_result:
        analysis["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        analysis["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        analysis["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        analysis["violence"] = {"severity": response.violence_result.severity}

    return analysis

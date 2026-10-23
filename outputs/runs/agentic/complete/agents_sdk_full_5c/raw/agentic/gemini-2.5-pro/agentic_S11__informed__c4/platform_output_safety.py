import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_content_safety(text_to_analyze: str):
    """
    Checks input text for harmful content using Azure AI Content Safety.

    Args:
        text_to_analyze: The text to be analyzed.
    
    Returns:
        The analysis result from the service.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
        return {
            "hate": response.hate_analysis.severity,
            "self_harm": response.self_harm_analysis.severity,
            "sexual": response.sexual_analysis.severity,
            "violence": response.violence_analysis.severity,
        }
    except HttpResponseError as e:
        print(f"Error analyzing text: {e}")
        raise

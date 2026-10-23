import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

def check_text_safety(text_to_check: str) -> dict:
    """
    Checks user-generated text fields for unsafe content using Azure AI Content Safety.

    :param text_to_check: The string content to analyze.
    :return: A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
    
    request = AnalyzeTextOptions(text=text_to_check)

    try:
        response = client.analyze_text(request)
        
        return {
            "hateResult": response.hate_result.severity if response.hate_result else 0,
            "selfHarmResult": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexualResult": response.sexual_result.severity if response.sexual_result else 0,
            "violenceResult": response.violence_result.severity if response.violence_result else 0,
        }
    except HttpResponseError as e:
        print(f"Azure AI Content Safety API error: {e.message}")
        raise

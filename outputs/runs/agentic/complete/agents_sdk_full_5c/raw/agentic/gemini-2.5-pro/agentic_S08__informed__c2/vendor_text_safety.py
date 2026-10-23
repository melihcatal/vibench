
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_vendor_text_safety(text: str) -> dict:
    """
    Moderates vendor notes or memo fields for harmful content using Azure AI Content Safety.

    Args:
        text: The text from the vendor notes to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text)
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        return {"error": str(e)}

    results = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }
    
    return results

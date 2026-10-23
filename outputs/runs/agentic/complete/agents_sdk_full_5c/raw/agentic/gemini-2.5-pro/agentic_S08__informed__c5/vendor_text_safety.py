"""
Moderate vendor notes or memo fields for safety.
"""
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_vendor_notes_safety(text: str) -> dict:
    """
    Uses Azure AI Content Safety to analyze text for harmful content.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(
        text=text,
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
        return {"error": f"Analyze text failed: {e.message}"}

    results = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }
    
    return results

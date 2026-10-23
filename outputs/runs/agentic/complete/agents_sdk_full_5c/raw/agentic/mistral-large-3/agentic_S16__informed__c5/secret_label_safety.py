from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os


def check_secret_label_safety(text: str) -> bool:
    """
    Checks secret labels and notes for unsafe text using Azure AI Content Safety.
    
    Args:
        text: The text to analyze for unsafe content.
        
    Returns:
        True if the text is safe, False otherwise.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    
    return all(
        result.severity < 2 for result in response.categories_analysis
    )
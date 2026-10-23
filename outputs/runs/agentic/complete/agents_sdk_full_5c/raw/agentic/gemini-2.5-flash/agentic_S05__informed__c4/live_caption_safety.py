import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

# Azure AI Content Safety configuration
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

def check_caption_safety(text: str) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))

    request = AnalyzeTextOptions(text=text)

    response = client.analyze_text(request)

    safety_results = {
        "hate": response.hate_result.severity if response.hate_result else -1,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else -1,
        "sexual": response.sexual_result.severity if response.sexual_result else -1,
        "violence": response.violence_result.severity if response.violence_result else -1,
    }
    return safety_results

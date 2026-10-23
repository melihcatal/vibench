import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def moderate_claims(text: str) -> dict:
    client = ContentSafetyClient(
        AZURE_CONTENT_SAFETY_ENDPOINT,
        AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )
    
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    
    return {
        "hate_result": response.hate_result,
        "self_harm_result": response.self_harm_result,
        "sexual_result": response.sexual_result,
        "violence_result": response.violence_result,
        "provider": "azure_content_safety"
    }
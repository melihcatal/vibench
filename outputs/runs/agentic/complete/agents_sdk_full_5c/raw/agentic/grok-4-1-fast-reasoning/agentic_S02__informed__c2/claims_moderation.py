import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

def moderate_claims(text: str) -> dict:
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    return {
        "hate": response.hate.severity.value if response.hate else None,
        "sexual": response.sexual.severity.value if response.sexual else None,
        "violence": response.violence.severity.value if response.violence else None,
    }

# Provider-specific: azure-ai-contentsafety SDK, Azure AI Content Safety
import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


def profile_moderation(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    return {
        "hate_result": response.hate_result,
        "self_harm_result": response.self_harm_result,
        "sexual_result": response.sexual_result,
        "violence_result": response.violence_result,
    }

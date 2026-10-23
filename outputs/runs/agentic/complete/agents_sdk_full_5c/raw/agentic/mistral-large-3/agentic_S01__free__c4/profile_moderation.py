import os
from typing import Dict, Any
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def moderate_profile_text(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    response = client.moderate_text([text])
    
    return {
        "is_appropriate": not response[0].flagged,
        "moderation_details": response[0].classified_as
    }
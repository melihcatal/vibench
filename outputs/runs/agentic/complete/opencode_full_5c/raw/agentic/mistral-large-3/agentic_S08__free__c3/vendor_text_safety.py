import os
from typing import Dict, Any
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Text Analytics credentials not configured")

    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    response = client.recognize_inappropriate_content([text])
    result = response[0]

    if result.is_error:
        raise Exception(f"Error in text moderation: {result.error}")

    return {
        "is_adult": result.classification_categories.adult_score > 0.5,
        "is_racy": result.classification_categories.racy_score > 0.5,
        "is_offensive": result.classification_categories.offensive_score > 0.5,
        "adult_score": result.classification_categories.adult_score,
        "racy_score": result.classification_categories.racy_score,
        "offensive_score": result.classification_categories.offensive_score,
    }

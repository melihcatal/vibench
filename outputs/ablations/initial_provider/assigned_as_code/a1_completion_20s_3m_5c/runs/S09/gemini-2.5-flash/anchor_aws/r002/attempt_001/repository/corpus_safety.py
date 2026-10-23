import os

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def corpus_safety(text_to_check, config=None):
    config = config or {}
    endpoint = config.get("azure_content_safety_endpoint")
    key = config.get("azure_content_safety_key")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be provided in config.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_check,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )
    
    response = client.analyze_text(request)

    safety_scores = {
        category.category.value: {"severity": category.severity} 
        for category in response.categories_analysis
    }
    
    return {"safety_scores": safety_scores}

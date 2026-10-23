import os
from typing import List, Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory
)
from azure.core.credentials import AzureKeyCredential


def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Check corpus texts for harmful content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not set")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    results = []
    
    for text in texts:
        request = AnalyzeTextOptions(text=text, categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ])
        response = client.analyze_text(request)
        
        results.append({
            "text": text,
            "hate_severity": response.hate_result.severity if response.hate_result else 0,
            "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
            "violence_severity": response.violence_result.severity if response.violence_result else 0
        })
    
    return results
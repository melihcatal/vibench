import os
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_unsafe_content(text: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.
    
    Expects AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    environment variables.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        return {"error": str(e)}

    analysis = {
        "hate": TextCategory.HATE,
        "self_harm": TextCategory.SELF_HARM,
        "sexual": TextCategory.SEXUAL,
        "violence": TextCategory.VIOLENCE,
    }
    
    results = {}
    for category, category_enum in analysis.items():
        for item in response.categories_analysis:
            if item.category == category_enum:
                results[category] = {"severity": item.severity}

    return results

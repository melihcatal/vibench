import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List

from safety_client import get_azure_content_safety_client
from safety_models import ModerationResult, TextCategory as SafetyTextCategory

def moderate_text(text: str) -> ModerationResult:
    client = get_azure_content_safety_client()

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
        categories = []
        if response.categories_analysis:
            for category in response.categories_analysis:
                categories.append(SafetyTextCategory(category=category.category, severity=category.severity))
        
        return ModerationResult(text=text, categories=categories)
    except Exception as e:
        # In a real application, sophisticated error handling would be here.
        # For this exercise, we re-raise or return an empty result.
        print(f"Error moderating text: {e}")
        return ModerationResult(text=text, categories=[])

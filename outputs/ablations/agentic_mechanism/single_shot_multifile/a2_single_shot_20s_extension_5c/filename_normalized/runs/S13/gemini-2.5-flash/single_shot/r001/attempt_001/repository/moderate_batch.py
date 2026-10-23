import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from typing import List

from safety_client import get_azure_content_safety_client
from safety_models import ModerationResult, BatchModerationInput, BatchModerationOutput, TextCategory as SafetyTextCategory

def moderate_batch(batch_input: BatchModerationInput) -> BatchModerationOutput:
    client = get_azure_content_safety_client()
    results: List[ModerationResult] = []

    for text_item in batch_input.texts:
        request = AnalyzeTextOptions(text=text_item)
        try:
            response = client.analyze_text(request)
            categories = []
            if response.categories_analysis:
                for category in response.categories_analysis:
                    categories.append(SafetyTextCategory(category=category.category, severity=category.severity))
            results.append(ModerationResult(text=text_item, categories=categories))
        except Exception as e:
            print(f"Error moderating text in batch: {text_item[:50]}... Error: {e}")
            results.append(ModerationResult(text=text_item, categories=[]))
            
    return BatchModerationOutput(results=results)

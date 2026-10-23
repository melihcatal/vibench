from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import AzureContentSafetyClient
from safety_models import BatchModerationRequest, BatchModerationResult, TextModerationResult
import os

def moderate_batch(batch_request: BatchModerationRequest, config: dict = None) -> List[BatchModerationResult]:
    config = config or {}
    client_wrapper = AzureContentSafetyClient(endpoint=config.get("AZURE_CONTENT_SAFETY_ENDPOINT"), api_key=config.get("AZURE_CONTENT_SAFETY_KEY"))
    client = client_wrapper.get_client()

    results: List[BatchModerationResult] = []
    for i, text in enumerate(batch_request.texts):
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
        
        moderation_results = []
        is_unsafe = False
        for category_analysis in response.categories_analysis:
            moderation_results.append(TextModerationResult(
                category=category_analysis.category,
                severity=category_analysis.severity
            ))
            if category_analysis.severity > 0:  # Assuming severity > 0 means it's unsafe to some degree
                is_unsafe = True

        results.append(BatchModerationResult(
            index=i,
            text=text,
            results=moderation_results,
            is_unsafe=is_unsafe
        ))
    return results

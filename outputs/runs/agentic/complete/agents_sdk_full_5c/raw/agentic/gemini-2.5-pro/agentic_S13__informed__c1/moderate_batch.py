from typing import List, Dict

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_azure_safety_client
from safety_models import ModerationResult, CategoryScore, BatchModerationResult

def moderate_batch(texts: List[str]) -> BatchModerationResult:
    """
    Moderates a batch of text messages and returns per-message decisions.
    """
    client = get_azure_safety_client()
    results: Dict[str, ModerationResult] = {}

    for text_input in texts:
        request = AnalyzeTextOptions(text=text_input)
        try:
            response = client.analyze_text(request)
            
            category_scores = {
                category.category.value: CategoryScore(severity=category.severity)
                for category in response.categories_analysis
            }

            results[text_input] = ModerationResult(
                is_safe=all(cat.severity == 0 for cat in response.categories_analysis),
                scores=category_scores,
                raw_response=response.to_dict(),
            )

        except HttpResponseError as e:
            # In a real app, you might want more robust error handling per-item
            print(f"Failed to analyze text '{text_input[:30]}...'. Reason: {e.reason}")
            results[text_input] = ModerationResult(is_safe=False, scores={}, raw_response={"error": str(e)})

    return BatchModerationResult(results=results)

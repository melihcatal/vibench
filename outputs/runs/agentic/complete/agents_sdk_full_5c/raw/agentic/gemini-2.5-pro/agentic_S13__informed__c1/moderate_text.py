from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import get_azure_safety_client
from safety_models import ModerationResult, CategoryScore

def moderate_text(text: str) -> ModerationResult:
    """
    Moderates a single piece of text for unsafe content.
    """
    client = get_azure_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        raise

    category_scores = {
        category.category.value: CategoryScore(
            severity=category.severity,
        )
        for category in response.categories_analysis
    }

    return ModerationResult(
        is_safe=all(cat.severity == 0 for cat in response.categories_analysis),
        scores=category_scores,
        raw_response=response.to_dict(),
    )

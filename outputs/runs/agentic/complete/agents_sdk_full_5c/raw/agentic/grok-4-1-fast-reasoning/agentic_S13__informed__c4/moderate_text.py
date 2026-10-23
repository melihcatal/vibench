from safety_client import get_azure_content_safety_client
from safety_models import ModerationResult
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    HateCategory,
    SelfHarmCategory,
    SexualCategory,
    ViolenceCategory
)

def moderate_text(text: str) -> ModerationResult:
    client = get_azure_content_safety_client()
    categories = [HateCategory(), SelfHarmCategory(), SexualCategory(), ViolenceCategory()]
    request = AnalyzeTextOptions(text=text, categories=categories)
    poller = client.analyze_text(request)
    result = poller.result()
    flagged = any(cat.result.severity.value != "safe" for cat in result.categories)
    categories_dict = {
        cat.name: {
            "score": cat.result.score,
            "severity": cat.result.severity.value
        } for cat in result.categories
    }
    return ModerationResult(input_text=text, flagged=flagged, categories=categories_dict)
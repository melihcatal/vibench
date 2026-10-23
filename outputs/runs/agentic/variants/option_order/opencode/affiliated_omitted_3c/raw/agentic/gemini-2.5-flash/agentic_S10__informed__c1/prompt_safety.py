from model_client import ModelClient
from model_models import ModerationRequest, ModerationResponse
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def analyze_text_for_safety(request: ModerationRequest) -> ModerationResponse:
    client = ModelClient.get_content_safety_client()
    request_body = AnalyzeTextOptions(text=request.text)

    response = client.analyze_text(request_body)

    flagged = False
    categories = {}

    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            categories[category_analysis.category.value] = {
                "severity": category_analysis.severity,
                "detected": category_analysis.severity > 0,
            }
            if category_analysis.severity > 0:
                flagged = True

    return ModerationResponse(flagged=flagged, categories=categories)

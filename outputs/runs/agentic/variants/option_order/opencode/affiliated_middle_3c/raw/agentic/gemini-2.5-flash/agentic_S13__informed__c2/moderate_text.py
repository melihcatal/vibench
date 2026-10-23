from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import TextModerationRequest, TextModerationResult


def moderate_text(request: TextModerationRequest) -> TextModerationResult:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]
    request_body = AnalyzeTextOptions(text=request.text, categories=categories)
    response = client.analyze_text(request_body)

    categories_analysis = []
    for category_result in response.categories_analysis:
        categories_analysis.append(
            {
                "category": category_result.category.value,
                "severity": category_result.severity,
            }
        )

    return TextModerationResult(categories_analysis=categories_analysis)

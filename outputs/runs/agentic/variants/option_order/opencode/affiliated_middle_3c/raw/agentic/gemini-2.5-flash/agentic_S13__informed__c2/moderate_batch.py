from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import TextModerationBatchRequest, TextModerationResult


def moderate_batch(
    request: TextModerationBatchRequest,
) -> dict[str, TextModerationResult]:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    results = {}
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    for i, text in enumerate(request.texts):
        request_body = AnalyzeTextOptions(text=text, categories=categories)
        response = client.analyze_text(request_body)

        categories_analysis = []
        for category_result in response.categories_analysis:
            categories_analysis.append(
                {
                    "category": category_result.category.value,
                    "severity": category_result.severity,
                }
            )
        results[f"message_{i}"] = TextModerationResult(
            categories_analysis=categories_analysis
        )

    return results

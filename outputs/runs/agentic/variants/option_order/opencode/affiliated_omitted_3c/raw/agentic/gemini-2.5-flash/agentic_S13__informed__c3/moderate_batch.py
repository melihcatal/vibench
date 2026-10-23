from safety_models import (
    BatchModerationRequest,
    BatchModerationResponse,
    TextModerationResult,
)
from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    client = get_content_safety_client()
    batch_results = []

    for text in request.texts:
        request_body = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request_body)

        text_results = []
        if response.categories_analysis:
            for category_analysis in response.categories_analysis:
                text_results.append(
                    TextModerationResult(
                        category=category_analysis.category.value,
                        severity=category_analysis.severity,
                        moderated=category_analysis.severity > 0,
                    )
                )
        batch_results.append(text_results)

    return BatchModerationResponse(results=batch_results)

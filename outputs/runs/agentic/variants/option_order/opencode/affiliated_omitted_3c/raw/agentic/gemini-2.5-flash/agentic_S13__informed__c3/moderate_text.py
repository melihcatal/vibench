from safety_models import (
    TextModerationRequest,
    TextModerationResponse,
    TextModerationResult,
)
from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text(request: TextModerationRequest) -> TextModerationResponse:
    client = get_content_safety_client()
    request_body = AnalyzeTextOptions(text=request.text)
    response = client.analyze_text(request_body)

    results = []
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            results.append(
                TextModerationResult(
                    category=category_analysis.category.value,
                    severity=category_analysis.severity,
                    moderated=category_analysis.severity > 0,
                )
            )

    # Azure Content Safety does not return an overall moderated status, so we derive it
    # If any category has a severity > 0, the text is considered moderated.
    overall_moderated = any(r.moderated for r in results)

    return TextModerationResponse(
        id="",  # Azure Content Safety does not return an ID for the analysis
        categories_analysis=results,
    )

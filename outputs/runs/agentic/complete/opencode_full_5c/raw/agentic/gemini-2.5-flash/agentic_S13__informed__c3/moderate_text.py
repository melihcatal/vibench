from safety_client import analyze_text_with_azure
from safety_models import (
    TextModerationRequest,
    TextModerationResult,
    TextModerationResponse,
)


def moderate_text(request: TextModerationRequest) -> TextModerationResponse:
    analysis_response = analyze_text_with_azure(request.text)

    results = []
    is_safe = True
    for r in analysis_response["results"]:
        results.append(
            TextModerationResult(category=r["category"], severity=r["severity"])
        )
        if (
            r["severity"] > 0
        ):  # Any severity greater than 0 means it's not safe in that category
            is_safe = False

    return TextModerationResponse(
        is_safe=is_safe, results=results, original_text=request.text
    )

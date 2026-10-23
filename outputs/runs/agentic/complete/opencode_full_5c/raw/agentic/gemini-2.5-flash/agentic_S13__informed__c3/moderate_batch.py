from safety_client import analyze_text_with_azure
from safety_models import (
    BatchModerationRequest,
    BatchModerationResponse,
    TextModerationResponse,
    TextModerationResult,
)


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    per_message_decisions = []
    for text in request.texts:
        analysis_response = analyze_text_with_azure(text)

        results = []
        is_safe = True
        for r in analysis_response["results"]:
            results.append(
                TextModerationResult(category=r["category"], severity=r["severity"])
            )
            if r["severity"] > 0:
                is_safe = False

        per_message_decisions.append(
            TextModerationResponse(is_safe=is_safe, results=results, original_text=text)
        )

    return BatchModerationResponse(per_message_decisions=per_message_decisions)

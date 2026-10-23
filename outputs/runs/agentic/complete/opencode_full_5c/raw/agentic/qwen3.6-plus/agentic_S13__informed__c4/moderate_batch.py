from azure.ai.contentsafety import ContentSafetyClient
from safety_client import (
    get_content_safety_client,
    build_analyze_text_payload,
    parse_analyze_text_response,
)
from safety_models import (
    ModerationRequest,
    ModerationResult,
    BatchModerationRequest,
    BatchModerationResult,
    moderation_result_from_parsed,
)


def moderate_batch(
    messages: list[str],
    categories: list[str] | None = None,
    client: ContentSafetyClient | None = None,
) -> BatchModerationResult:
    if client is None:
        client = get_content_safety_client()
    results: list[ModerationResult] = []
    for msg in messages:
        payload = build_analyze_text_payload(text=msg, categories=categories)
        response = client.analyze_text(payload)
        parsed = parse_analyze_text_response(response)
        result = moderation_result_from_parsed(
            text=msg,
            parsed=parsed,
            raw_response=response,
        )
        results.append(result)
    total_flagged = sum(1 for r in results if r.overall_flagged)
    total_safe = len(results) - total_flagged
    return BatchModerationResult(
        results=results,
        total_flagged=total_flagged,
        total_safe=total_safe,
    )


def moderate_batch_from_request(
    request: BatchModerationRequest,
    client: ContentSafetyClient | None = None,
) -> BatchModerationResult:
    return moderate_batch(
        messages=[m.text for m in request.messages],
        categories=request.messages[0].categories if request.messages else None,
        client=client,
    )
